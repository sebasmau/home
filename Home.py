import streamlit as st
import pyrebase
import pandas as pd
import time

####PAGE CONFIG

st.set_page_config(
    page_title="Sébastien's app",
    page_icon="🏠",
    layout='wide'
)

#### add CSS style and hide unneeded streamlit visuals
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.write("hello little app")
