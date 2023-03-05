import streamlit as st
import pyrebase
import time
import webbrowser
import altair as alt
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
        st.session_state['userID'] = None

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
        login = st.form_submit_button("Login",type="primary")
    

    if login:
        try:
            signin = st.session_state['firebase'].auth().sign_in_with_email_and_password(email,pw)
            st.session_state['logged_in'] = True
            st.session_state['password_reset'] = False
            st.session_state['userID'] = signin['localId']
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
    if st.session_state['logged_in'] == True:
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


def solarpanels():
    years = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
    fixed_investment = 2130
    variable_investment = 422
    price_high = 0.5
    price_low = 0.3
    self_consumption = 0.3
    kWh_year_solarpanel = 293
    CO2_kWh = 300
    with st.expander(label='Zonnepanelen'):
        solarcol1,solarcol2 = st.columns([1.1,2])

        solarcol1.write("### Zonnepanelen")
        solarpanels = solarcol1.number_input('Optimaal aantal zonnepanelen',min_value= 6,max_value=30, value=12)

        
        solarinvestment = solarpanels * variable_investment + fixed_investment
        profit = [round(i * (solarpanels*kWh_year_solarpanel*(price_high*self_consumption+price_low*(1-self_consumption)))-solarinvestment) for i in years]
        solarcol2.write("### Terugverdientijd")
        source = pd.DataFrame({"Jaren":years,"Winst (€)":profit})#.set_index("Jaren")
        chartalt = alt.Chart(source).mark_bar().encode(
            x="Jaren:O",
            y="Winst (€):Q",
            # The highlight will be set on the result of a conditional statement
            color=alt.condition(
                alt.datum["Winst (€)"] > 0,  # If the year is 1810 this test returns True,
                alt.value('#90ee90'),     # which sets the bar orange.
                alt.value('red')   # And if it's not true it sets the bar steelblue.
            )
        ).properties(height=450)
        solarcol2.altair_chart(chartalt, use_container_width=True)
        #solarcol2.bar_chart(source.set_index("Jaren"),height=500)


        solarcol1.metric("Geschatte prijs voor deze installatie",f"{solarinvestment} €")
        solarcol1.metric("Terugverdientijd",f"{round(solarinvestment / (solarpanels*kWh_year_solarpanel*(price_high*self_consumption+price_low*(1-self_consumption))),1)} jaar")
        solarcol1.metric("Winst na 25 jaar",f"{round(profit[24])} €")
        solarcol1.metric("CO2 besparing na 25 jaar",f"{round(solarpanels*kWh_year_solarpanel*CO2_kWh*25/1000)} kg")
        if solarcol1.button('Meer info?'):
            webbrowser.open_new_tab("https://www.hs-powersolutions.be/")

    
    
st.write("#### Top besparingstips voor jou")
solarpanels()