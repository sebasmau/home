import streamlit as st
import StreamlitAppBlocks 


StreamlitAppBlocks.login_screen()
####PAGE CONFIG

st.set_page_config(
    page_title="Sébastien Mauroo",
    page_icon="🪵",
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



#### pre-fill session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False





#SIDEBAR
period_raw = st.sidebar.selectbox('Periode',['Voorbije 24 uur','Voorbije 2 uur','Voorbije 7 dagen'])
