import streamlit as st
import pyrebase
import pandas as pd
import time

####PAGE CONFIG

st.set_page_config(
    page_title="MeterT",
    page_icon="⚡",
    layout='wide'
)

#### add CSS style and hide unneeded streamlit visuals
with open('dashboard/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

####LOGIN CODE####


if 'firebase' not in st.session_state:
        config = {"apiKey":st.secrets["firebase_credentials"]["apiKey"],"authDomain":st.secrets["firebase_credentials"]["authDomain"],"storageBucket":st.secrets["firebase_credentials"]["storageBucket"],"databaseURL":st.secrets["firebase_credentials"]["databaseURL"]}
        st.session_state['firebase'] = pyrebase.initialize_app(config)

if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

if 'password_reset' not in st.session_state:
        st.session_state['password_reset'] = False

if 'create_account' not in st.session_state:
        st.session_state['create_account'] = False

if st.session_state['logged_in'] == False and st.session_state['create_account'] == False:  ###sign in screen 
    with st.form("Inloggen"):
        st.subheader("Login")
        email = st.text_input("Emailadres")
        pw = st.text_input("Wachtwoord", type="password")
        login = st.form_submit_button("Login")
    
    ####button to show create account instead
    if st.button("Account aanmaken"):
        st.session_state['password_reset'] = False
        st.session_state['create_account'] = True
        st.experimental_rerun()

    if login:
        try:
            signin = st.session_state['firebase'].auth().sign_in_with_email_and_password(email,pw)
            st.session_state['logged_in'] = True
            st.session_state['password_reset'] = False
        except:
            st.error("verkeerd wachtwoord")
            st.session_state['password_reset'] = True

    if st.session_state['password_reset'] == True:
        if st.button("Verander je wachtwoord"):
            try:
                st.session_state['firebase'].auth().send_password_reset_email(email)
                st.markdown(f"Email verzonden naar {email}")
                st.caption(f"Deze email kan ook in je spam folder te vinden zijn")
            except:
                st.markdown(f"Niet mogelijk om een email te sturen naar: {email}, probeer later opnieuw")
    
    if st.session_state['logged_in'] == True:
        st.experimental_rerun()
    else:
        st.stop()

elif st.session_state['logged_in'] == False and st.session_state['create_account'] == True:  ###create password button
    with st.form("Account aanmaken"):
        st.subheader("Account aanmaken")
        email = st.text_input("Emailadres")
        pw = st.text_input("Wachtwoord", type="password")
        login = st.form_submit_button("Enter")

    ####button to show login screen instead

    if st.button("Inloggen met bestaand account"):
        st.session_state['password_reset'] = False
        st.session_state['create_account'] = False
        st.experimental_rerun()

    ####check email and password
    if login:
        if '@' not in email or '.' not in email:
            st.warning("Vul een geldig emailadres in")
            st.stop()
        elif len(pw)<6:
            st.info("Wachtwoord moet minimaal 7 karakters lang zijn")
            st.stop()
        else:
            try:
                signin = st.session_state['firebase'].auth().create_user_with_email_and_password(email,pw)
                st.session_state['logged_in'] = True
                st.session_state['password_reset'] = False
                st.experimental_rerun()
            except:
                st.info("Aanmaken van een account niet gelukt, probeer later opnieuw")
                st.stop()
    else:
        st.stop()
    


####################################
###ACTUAL APP
####################################

###functions

@st.cache_data(show_spinner="Analyseren hoe je geld kan besparen...")
def interpret_csv_dataset(dt):
    ###get start period
    dt['start_time'] = pd.to_datetime(dt.iloc[:,0] + " " + dt.iloc[:,1])

    ###get end period
    dt['end_time'] = pd.to_datetime(dt.iloc[:,2] + " " + dt.iloc[:,3])

    #get repeated parameters
    EAN_code = dt["EAN"].iloc[0].replace('=','').replace('"','')
    Meter_code = dt["Meter"].iloc[0]
    Meter_type = dt["Metertype"].iloc[0]
    Power_unit = dt["Eenheid"].iloc[0]
    Time_unit = (dt["end_time"].iloc[0] - dt["start_time"].iloc[0]).seconds/60 ##15 bij kwartier waarden, 60 bij uurwaarden
    Data_period = (dt["start_time"].iloc[-1] - dt["start_time"].iloc[0]).round('d').days

    #get rid of useless columns
    dt = dt.dropna()[['start_time','end_time','Volume','Register']]

    ######injection analysis

    #Estimated solar capacity
    var1 = dt[dt['Register'].str.contains('Injectie')]['Volume'].nlargest(3) ###largest 3 injectinos
    Estimated_generation_capacity = var1.mean()*60/Time_unit ###60/Time_unit converts kWh towards kW

    #Has solar panels
    Has_solar_panels = True if Estimated_generation_capacity >= 0.6 else False  ###2 solar panels = +-600W

    return dt

@st.cache_data(show_spinner="Analyseren hoe je geld kan besparen...")
def create_graph_data(dt):
    graphtable = dt.pivot_table(index='end_time', columns='Register', values='Volume',aggfunc='mean').fillna(0)
    graphtable['Afname'] = graphtable['Afname Dag'] + graphtable['Afname Nacht']
    graphtable['Injectie'] = graphtable['Injectie Dag'] + graphtable['Injectie Nacht']
    return graphtable[['Afname','Injectie']]


st.title("Welcome bij MeterT 👋")
st.write("\n")



uploaded_file = st.file_uploader("Plaats hier je Fluvius verbruik bestand",accept_multiple_files=False,type=["csv"])

if uploaded_file is not None:
    try:
        dt = pd.read_csv(uploaded_file,delimiter=';')
        dt = interpret_csv_dataset(dt)
        st.line_chart(create_graph_data(dt))
    except Exception as e:
        st.write(e)
        #st.warning("Dit is geen gebruikersdata van Fluvius")




