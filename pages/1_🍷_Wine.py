import streamlit as st
import pandas as pd
import time

####PAGE CONFIG

st.set_page_config(
    page_title="Wine",
    page_icon="🍷",
    layout='wide'
)

#### add CSS style and hide unneeded streamlit visuals
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.write("hello little app")

winelist = pd.read_csv("winedatabase.csv",delimiter=';',decimal=',')

edited_winelist = st.data_editor(
    winelist,
    num_rows="dynamic",
    column_order = [
        "naam",
        "jaar",
        "type",
        "land",
        "regio",
        "stock",
        "prijs",
        "score_sebastien",
        "vivino_rating",
        "soepel_tanninerijk",
        "licht_stevig",
        "droog_zoet",
        "rond_fris",
        "cadeau",
        "schenker"
    ],
    column_config={
        "naam": "Wijnnaam",
        "jaar": st.column_config.NumberColumn(
            "Botteljaar",
            help="het jaar waarin de fles werd gebotteld",
            min_value=1980,
            max_value=2030,
            step=1,
            format="%d"
        ),
        "type": "Type wijn",
        "stock": st.column_config.NumberColumn(
            "Aantal",
            help="Aantal flessen momenteel op stock",
            step=1,
            format="%d"
        ),
        "land": st.column_config.SelectboxColumn(
            "Land",
            help="Land van oorsprong van de wijn",
            options=[
                "🇫🇷 Frankrijk",
                "🇧🇪 België",
                "🇩🇪 Duitsland",
                "🇪🇸 Spanje",
                "🇦🇹 Oostenrijk",
            ],
        ),
        "prijs": st.column_config.NumberColumn(
            "Fles prijs",
            help="Aankoop prijs van deze wijn",
            format="€ %.2f"
        ),
        "score_sebastien": "Mijn rating",
        "vivino_rating": "Vivino",
        "soepel_tanninerijk": "Tannines",
        "licht_stevig": "Sterkte",
        "droog_zoet": "Zoetheid",
        "rond_fris": "Frisheid"
    },
    hide_index=True
)

if st.button("save",type="primary", use_container_width=True):
    edited_winelist.to_csv("winedatabase.csv",sep=';',decimal=",")