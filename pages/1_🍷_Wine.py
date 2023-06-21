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
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.write("hello little app")

winelist = pd.read_csv("winedatabase.csv",delimiter=';',decimal=',')
edited_winelist = st.data_editor(
    winelist,
    hide_index=True,
    num_rows="dynamic",
    column_config={
        "naam": "Wijnnaam",
        "jaar": st.column_config.NumberColumn(
            "Botteljaar",
            width="small",
            help="het jaar waarin de fles werd gebotteld",
            min_value=1980,
            max_value=2030,
            step=1,
            format="%d"
        ),
        "type": "Type wijn",
        "Stock": st.column_config.NumberColumn(
            "Aantal",
            width="small",
            help="Aantal flessen momenteel op stock",
            step=1,
            format="%d"
        ),
        "Land": st.column_config.SelectboxColumn(
            "Land",
            help="Land van oorsprong van de wijn",
            width="small",
            options=[
                "🇫🇷 Frankrijk",
                "🇧🇪 België",
                "🇩🇪 Duitsland",
                "🇪🇸 Spanje",
                "🇦🇹 Oostenrijk",
            ],
        )
        "prijs": st.column_config.NumberColumn(
            "Fles prijs",
            width="small",
            help="Aankoop prijs van deze wijn",
            format="€ %d"
        ),
    }
)

if st.button("save",type="primary", use_container_width=True):
    edited_winelist.to_csv("winedatabase.csv",sep=';',decimal=",")