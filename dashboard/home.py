import streamlit as st

####PAGE CONFIG

st.set_page_config(
    page_title="Sébastien Mauroo",
    page_icon="🪵",
    layout='wide'
)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

#SIDEBAR
period_raw = st.sidebar.selectbox('Periode',['Voorbije 24 uur','Voorbije 2 uur','Voorbije 7 dagen'])
period_translator = {'Voorbije 24 uur':(24,60),'Voorbije 2 uur':(2,1),'Voorbije 7 dagen':(168,900)} ##number of hours, aggregation in seconds
period = period_translator[period_raw]