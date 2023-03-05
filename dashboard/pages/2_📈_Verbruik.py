import streamlit as st
import pyrebase
import time
import pandas as pd

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

if 'UserID' not in st.session_state:
        st.session_state['userID'] = "Unknown"

if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

if 'password_reset' not in st.session_state:
        st.session_state['password_reset'] = False

if 'create_account' not in st.session_state:
        st.session_state['create_account'] = False

st.write(st.session_state['userID'])

if st.session_state['logged_in'] == False and st.session_state['create_account'] == False:  ###sign in screen 
    with st.form("Inloggen"):
        st.subheader("Login")
        email = st.text_input("Emailadres")
        pw = st.text_input("Wachtwoord", type="password")
        login = st.form_submit_button("Login",type="primary")
    

    if login:
        try:
            signin = st.session_state['firebase'].auth().sign_in_with_email_and_password(email,pw)
            st.session_state['logged_in'] = True
            st.session_state['password_reset'] = False
            st.session_state['userID'] = signin['localId']
            st.write(st.session_state['userID'])
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
                st.info(f"Niet mogelijk om een email te sturen naar: {email}, probeer later opnieuw")
    

    ####button to show create account instead
    if st.button("Account aanmaken"):
        st.session_state['password_reset'] = False
        st.session_state['create_account'] = True
        st.experimental_rerun()

    
    ####rerun script to show real page after succesfull login
    if st.session_state['logged_in']:
        st.write(st.session_state['userID'])
        time.sleep(10)
        st.experimental_rerun()
    else:
        st.stop()

elif st.session_state['logged_in'] == False and st.session_state['create_account'] == True:  ###create password button
    with st.form("Account aanmaken"):
        st.subheader("Account aanmaken")
        email = st.text_input("Emailadres")
        pw = st.text_input("Wachtwoord", type="password")
        login = st.form_submit_button("Enter",type="primary")

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
                st.session_state['userID'] = signin['localId']
            except:
                st.info("Aanmaken van een account niet gelukt, probeer later opnieuw")
                st.stop()
        st.experimental_rerun()
    else:
        st.stop()
    



###ACTUAL APP
st.write(st.session_state['userID'])

tab1, tab2 = st.tabs(["Fluvius - Digitale meter", "Invencado - Smart Meter"])


with tab1:

    @st.cache_data(show_spinner="Analyseren hoe je geld kan besparen...")
    def interpret_csv_dataset(uploaded_file):
        st.write(st.session_state['userID'])
        ###translate csv into dataframe and create dict to be save
        dt = pd.read_csv(uploaded_file,delimiter=';',decimal=',')
        EAN_data = {}

        ###get start period
        dt['start_time'] = pd.to_datetime(dt.iloc[:,0] + " " + dt.iloc[:,1],format='%d-%m-%Y %H:%M:%S')

        ###get end period
        dt['end_time'] = pd.to_datetime(dt.iloc[:,2] + " " + dt.iloc[:,3],format='%d-%m-%Y %H:%M:%S')

        #get file parameters
        EAN_data['EAN_code'] = dt["EAN"].iloc[0].replace('=','').replace('"','')
        EAN_data['Meter_code'] = dt["Meter"].iloc[0]
        EAN_data['Meter_type'] = dt["Metertype"].iloc[0]
        EAN_data['Power_unit'] = dt["Eenheid"].iloc[0]
        EAN_data['Time_unit (m)'] = (dt["end_time"].iloc[0] - dt["start_time"].iloc[0]).seconds/60 ##15 bij kwartier waarden, 60 bij uurwaarden
        EAN_data['Available_period (d)'] = (dt["start_time"].iloc[-1] - dt["start_time"].iloc[0]).round('d').days
        EAN_data['start_time'] = dt["start_time"].iloc[0].strftime('%d-%m-%Y %H:%M:%S')
        EAN_data['end_time'] = dt["end_time"].iloc[-1].strftime('%d-%m-%Y %H:%M:%S')

        #get rid of useless columns
        dt = dt.dropna()[['start_time','end_time','Volume','Register']]

        #get calulated parameters
        largest_injections = dt[dt['Register'].str.contains('Injectie')]['Volume'].nlargest(5) ###largest 5 injections found
        EAN_data['Estimated_generation_capacity (kW)'] = largest_injections.mean()*60/EAN_data['Time_unit (m)'] ###60/Time_unit converts kWh towards kW
        EAN_data['Has_solar_panels'] = True if EAN_data['Estimated_generation_capacity (kW)'] >= 0.6 else False  ###2 solar panels = +-600W


        #get injection and usage
        EAN_data['Afname Dag (kWh)'] = dt[dt['Register'].str.contains('Afname Dag')]['Volume'].sum()
        EAN_data['Afname Nacht (kWh)'] = dt[dt['Register'].str.contains('Afname Nacht')]['Volume'].sum()
        EAN_data['Injectie Dag (kWh)'] = dt[dt['Register'].str.contains('Injectie Dag')]['Volume'].sum()
        EAN_data['Injectie Nacht (kWh)'] = dt[dt['Register'].str.contains('Injectie Nacht')]['Volume'].sum()
        vart = dt.set_index('start_time').between_time('10:00','16:00')
        EAN_data['Afname Dag 10_16 (kWh)'] = vart[vart['Register'].str.contains('Afname Dag')]['Volume'].sum()
        EAN_data['Injectie Dag 10_16 (kWh)'] = vart[vart['Register'].str.contains('Injectie Dag')]['Volume'].sum()

        #get peak percentile sensitivity
        sensitivity = [0.9,0.95,0.99,0.999,0.9999,1]
        afname_piek = []
        for i in sensitivity:
            afname_piek.append(dt[dt['Register'].str.contains('Afname')]['Volume'].quantile(i)*60/EAN_data['Time_unit (m)'])
        EAN_data['Afname piek percentielen (kW)'] = afname_piek


        sensitivity = [0,0.01,0.05,0.1,0.2,0.3]
        afname_nacht_dal = []
        for i in sensitivity:
            afname_nacht_dal.append(dt[dt['Register'].str.contains('Afname')]['Volume'].quantile(i)*60/EAN_data['Time_unit (m)'])
        EAN_data['Afname Nacht dal percentielen (kW)'] = afname_nacht_dal



        #write to database
        st.session_state['firebase'].database().child("user").child(st.session_state['userID']).child(EAN_data['EAN_code']).set(True)
        st.session_state['firebase'].database().child("fluvius_data").child(EAN_data['EAN_code']).set(EAN_data)
        

    @st.cache_data(show_spinner="Analyseren hoe je geld kan besparen...")
    def create_graph_data(dt):
        graphtable = dt.pivot_table(index='end_time', columns='Register', values='Volume',aggfunc='mean').fillna(0)
        graphtable['Afname'] = graphtable['Afname Dag'] + graphtable['Afname Nacht']
        graphtable['Injectie'] = graphtable['Injectie Dag'] + graphtable['Injectie Nacht']
        return graphtable[['Afname','Injectie']]


    ####actual app

    uploaded_file = st.file_uploader("Plaats hier je Fluvius verbruik bestand",accept_multiple_files=False,type=["csv"])


    ##initialize data upload
    if uploaded_file is not None:
        try:
            st.write(st.session_state['userID'])
            interpret_csv_dataset(uploaded_file)
            st.write(st.session_state['userID'])
            st.success("Analyse naar hoe je geld kan besparen was succesvol, de resultaten kan je zien bij '"'🔎 Energie audit'"'")
            st.balloons()
        except:
            st.warning("Deze data kon niet ingelezen worden, de juiste data kan je vinden op de website van [Fluvius](https://www.fluvius.be/nl/thema/meters-en-meterstanden/digitale-meter/hoe-mijn-energieverbruik-online-raadplegen)")




with tab2:
    with st.form("Maak verbinding met je '"'Invencado Smart Meter'"'"):
        st.subheader("Maak verbinding met je '"'Invencado Smart Meter'"'")
        mac_address = st.text_input("Meternummer",placeholder="Bijvoorbeeld: '7ab0ae642979'",help="Je meternummer kan je terugvinden op je Invencado Smart Meter, het is de code die op de kabel geschreven is")
        challenge_code = st.text_input("challengecode", type="password",help="De beveiligingscode kan je terugvinden op het instructieformulier die bij de meter in de doos zat (momenteel is dit 123)")
        connect_to_meter = st.form_submit_button("Verbinding maken",type="primary")

    if connect_to_meter:
        try:
            all_existing_meter_macs = list(st.session_state['firebase'].database().child("metermac").shallow().get().val()) ##get all key values (shallow), and then make a readable list out of the val() you read
            if mac_address in all_existing_meter_macs:
                st.success("Deze meter is actief, maar kan nog geen data doorsturen naar deze website")
            elif challenge_code != "123":
                st.error("Verkeerde challenge code (tip het is 123)")
        except:
            st.error("Onbekend meternummer")
         