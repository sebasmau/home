import streamlit as st
import StreamlitAppBlocks 

####PAGE CONFIG

st.set_page_config(
    page_title="Sébastien Mauroo",
    page_icon="🪵",
    layout='wide'
)


if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

if st.session_state['logged_in'] == False:
    StreamlitAppBlocks.login_screen()


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
