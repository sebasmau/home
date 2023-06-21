import streamlit as st
import pyrebase
import pandas as pd
import time

####PAGE CONFIG

st.set_page_config(
    page_title="Kleine Houtakker",
    page_icon="⚡",
    layout='wide'
)

#### add CSS style and hide unneeded streamlit visuals
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.write("hello little app")

winelist = pd.read_csv("winedatabase.csv",delimiter=';',decimal=',')
edited_winelist = st.data_editor(winelist)

if st.button("save",type="primary", use_container_width=True):
    edited_winelist.to_csv(sep=';',decimal=",")