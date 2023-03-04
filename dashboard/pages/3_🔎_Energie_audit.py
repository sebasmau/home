import streamlit as st
import pyrebase
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
        login = st.form_submit_button("Login",type="primary")
    

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
            except:
                st.info("Aanmaken van een account niet gelukt, probeer later opnieuw")
                st.stop()
        st.experimental_rerun()
    else:
        st.stop()
    



###ACTUAL APP


tab1, tab2, tab3 = st.tabs(["Algemene instellingen", "Mijn electriciteits leverancier", "Mijn elektrische installatie"])


with tab1:
    st.write("#### Algemene gegevens")
    st.text_input('Mijn adres',placeholder='Bijvoorbeeld: Koekoekstraat 70, Melle')
    st.selectbox("Energie audit: details",options=["Normaal","Geef me alle technische details!"])



with tab2:
    st.write("#### Energie leverancier")
    lev = st.selectbox('Wie is uw huidige energie leverancier',['Engie Electrabel','Luminus',"Mega","Total Energies","Eneco","Bolt",'Ik weet het niet','Andere'])
    if lev == "Luminus":
        contract = st.selectbox('Wat is uw huidig contract?',['Afzetterij ECO','Afzetterij Premium'])

    st.select_slider("Bent u tevreden van uw huidige energie leverancier?",['Niet tevreden','Eerder niet tevreden',"Neutraal","Tevreden","Zeer tevreden"],value='Neutraal')

    st.write("#### Energie prijs")
    typetarief = st.selectbox('Heeft u een dag/nacht tarief of een dag tarief',['Dag/Nacht tarief','Dag tarief','Ik weet het niet','Andere'])

    if typetarief == 'Dag/Nacht tarief':
        st.slider("Dag tarief (€)",min_value=0.0,max_value=1.5,value=0.90)
        st.slider("Nacht tarief (€)",min_value=0.0,max_value=1.5,value = 0.60)
        st.slider("Injectie tarief (€)",min_value=0.0,max_value=1.5,value = 0.40)
    elif typetarief == 'Dag tarief':
        st.slider("tarief (€)",min_value=0.0,max_value=1.5,value=0.70)
        st.slider("Injectie tarief (€)",min_value=0.0,max_value=1.5,value = 0.40)

with tab3:
    st.write("#### Zonnepanelen")
    zonp = st.selectbox('Heeft u zonnepanelen',['Ik heb geen zonnepanelen','Ik heb zonnepanelen','ik wil graag zonnepanelen'])
    if zonp == 'Ik heb zonnepanelen':
        st.number_input('Aantal zonnepanelen', 0,20)
        st.slider('Vermogen per zonnepaneel (Wp)',200,500,step=10,value=350)

    st.write("#### Thuisbatterij")
    zonp = st.selectbox('Heeft u een thuisbatterij',['Ik heb geen thuisbatterij','Ik heb een thuisbatterij','ik wil graag een thuisbatterij'])

if st.button("Gegevens opslaan"): 
    #with open('users.yaml', 'w') as f:
    #data = yaml.dump(config, f)
    st.balloons()