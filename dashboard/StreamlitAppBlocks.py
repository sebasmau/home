import streamlit as st
import pyrebase


def init_firebase():
    if 'firebase' not in st.session_state:
        st.secrets["db_username"]
        config = {"apiKey":st.secrets["apiKey"],"authDomain":st.secrets["authDomain"],"storageBucket":st.secrets["storageBucket"],"databaseURL":st.secrets["databaseURL"]}
        st.session_state['firebase'] = pyrebase.initialize_app(config)

def login_screen():

    init_firebase()

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    with st.form("Inloggen"):
        st.subheader("Login")
        email = st.text_input("Emailadres")
        pw = st.text_input("Wachtwoord", type="password")
        login = st.form_submit_button("Login")
    
    if login:
        try:
            signin = st.session_state['firebase'].auth().sign_in_with_email_and_password(email,pw)
            st.succes("Login succesvol")
        except:
            st.succes("verkeerd wachtwoord")