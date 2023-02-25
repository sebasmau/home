import streamlit as st
import StreamlitAppBlocks
import pyrebase
import time

####PAGE CONFIG

st.set_page_config(
    page_title="Sébastien Mauroo",
    page_icon="🪵",
    layout='wide'
)


####LOGIN CODE####

if 'firebase' not in st.session_state:
        config = {"apiKey":st.secrets["firebase_credentials"]["apiKey"],"authDomain":st.secrets["firebase_credentials"]["authDomain"],"storageBucket":st.secrets["firebase_credentials"]["storageBucket"],"databaseURL":st.secrets["firebase_credentials"]["databaseURL"]}
        st.session_state['firebase'] = pyrebase.initialize_app(config)

if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

if st.session_state['logged_in'] == False:   
    with st.form("Inloggen"):
        st.subheader("Login")
        email = st.text_input("Emailadres")
        pw = st.text_input("Wachtwoord", type="password")
        login = st.form_submit_button("Login")
        
    if login:
        try:
            signin = st.session_state['firebase'].auth().sign_in_with_email_and_password(email,pw)
            st.success("Login succesvol")
            st.session_state['logged_in'] = True
            time.sleep(3)
            st.experimental_rerun()
        except:
            st.error("verkeerd wachtwoord")
    st.stop()



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


st.title("Welcome to the App!")





#SIDEBAR
period_raw = st.sidebar.selectbox('Periode',['Voorbije 24 uur','Voorbije 2 uur','Voorbije 7 dagen'])
