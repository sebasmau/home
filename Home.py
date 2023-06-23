import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
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
            Header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.write("hello little app")


# Use the secret key "firebase" to get the firebase account key
cred = credentials.Certificate(st.secrets["firestore_credentials"])
firebase_admin.initialize_app(cred)

# Create a reference to the firestore database
db = firestore.client()

# Create a reference to the "posts" collection
posts_ref = db.collection("winecollection")

# Add a new document to the collection with some data
new_post = posts_ref.document()
new_post.set({
    "title": "Hello Streamlit",
    "content": "This is a test post",
    "timestamp": firestore.SERVER_TIMESTAMP
})