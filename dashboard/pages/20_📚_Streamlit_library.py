import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
import pydeck as pdk
import influxdb_methods as infldb
import datetime
from urllib.error import URLError

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(Invencado_logo);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "test";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(
    page_title="Library",
    page_icon="📚",
    layout='wide'
)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)

if 'user' not in st.session_state:
    st.session_state['user'] = ""

if st.session_state['user'] != "sebastien.mauroo@outlook.com":
    st.warning("Under construction")
    st.stop()

add_logo()


st.title ("this is the app title",anchor="titletest")
st.header("this is the markdown")
st.markdown("this is the header")
st.subheader("this is the subheader")
st.caption("this is the caption")
st.code("x=2021")
st.latex(r''' a+a r^1+a r^2+a r^3 ''')
st.metric("Power usage","23 kWh", "-2% Y2Y")
st.header("Widgets")

st.checkbox('yes')
if st.button('Balloons!',help="Hey ik wou even testen hoelang de tooltip hier kon zijn, dus ja even door zeveren dan maar. Aardappelen zijn geel, aardbeien zijn eerst groen, en dan pas rood"): st.balloons()
st.radio('Pick your gender',['Male','Female'])
st.selectbox('Pick your gender',['Male','Female'])
st.multiselect('choose a planet',['Jupiter', 'Mars', 'neptune'])
st.select_slider('Pick a mark', ['Bad', 'Good', 'Excellent'])
st.slider('Pick a number', 0,50)
st.slider("range",min_value=0,max_value=50,value=(5,12))
st.date_input("date input",value=(datetime.datetime(2022,12,1,10),datetime.datetime(2022,12,10,11)))
start_time = st.time_input("start time")
st.time_input("end time")

st.number_input('Pick a number', 0,10)
st.text_input('Email address')
st.date_input('Travelling date')
st.time_input('School time')
st.text_area('Description')
st.file_uploader('Upload a photo')
st.color_picker('Choose your favorite color')
st.file_uploader("upload file here",accept_multiple_files=True,type=["csv"])

st.camera_input("cheese")
#st.snow()
st.progress(10)
#with st.spinner('Wait for it...'):
#    time.sleep(10)


st.success("You did it !")
st.error("Error")
st.warning("Warning")
st.info("It's easy to build a streamlit app")
st.exception(RuntimeError("RuntimeError exception"))

df= pd.DataFrame(
    np.random.randn(10, 2),
    columns=['x', 'y'])
st.line_chart(df)
st.bar_chart(df)
st.area_chart(df)


my_expander = st.expander(label='Expand me')
with my_expander:
    'Hello there!'
    clicked = st.button('Click me!')

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with st.container():
   st.write("This is inside the container")

   # You can call any Streamlit command, including custom components:
   st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)

    ---

    **This is bold text**
    *This text is italicized*
    ~~This was mistaken text~~
    **This text is _extremely_ important**\n
    <sub>This is a subscript text</sub>
    <sup>This is a superscript text</sup>

    > Single line quote
    >> Nested quote
    >> multiple line
    >> quote

    ```
    sudo npm install vsoagent-installer -g  
    ```
    ---
    | Heading 1 | Heading 2 | Heading 3 |  
    |-----------|:-----------:|-----------:|  
    | Cell A1 | Cell A2 | Cell A3 |  
    | Cell B1 | Cell B2 | Cell B3<br/>second line of text |  

    1. First item.
    1. Second item.
    1. Third item.

    - [ ] A  
    - [ ] B  
    - [ ] C  
    - [x] A  
    - [x] B  
    - [x] C
    :smile:
    :angry:  
    [Link to all vega graphs](https://altair-viz.github.io/gallery/index.html)
"""
)



series = pd.DataFrame({
  'year': ['2010', '2011', '2012', '2013','2010', '2011', '2012', '2013'],
  'animal': ['antelope', 'antelope', 'antelope', 'antelope', 'velociraptor', 'velociraptor', 'velociraptor', 'velociraptor',],
  'count': [8, 6, 3, 1, 2, 4, 5, 5]
})

# Basic Altair line chart where it picks automatically the colors for the lines
basic_chart = alt.Chart(series).mark_line().encode(
    x='year',
    y='count',
    color='animal',
    # legend=alt.Legend(title='Animals by year')
)

# Custom Altair line chart where you set color and specify dimensions
custom_chart = alt.Chart(series).mark_line().encode(
    x='year',
    y='count',
    color=alt.Color('animal',
            scale=alt.Scale(
                domain=['antelope', 'velociraptor'],
                range=['blue', 'red'])
                )
).properties(
    width=900,
    height=500
)

st.altair_chart(basic_chart)
st.altair_chart(custom_chart)


st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.002)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")


st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")
st.write(
    """This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)


@st.experimental_memo
def from_data_file(filename):
    url = (
        "http://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename
    )
    return pd.read_json(url)


try:
    ALL_LAYERS = {
        "Bike Rentals": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("bike_rental_stats.json"),
            get_position=["lon", "lat"],
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
        ),
        "Bart Stop Exits": pdk.Layer(
            "ScatterplotLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="[exits]",
            radius_scale=0.05,
        ),
        "Bart Stop Names": pdk.Layer(
            "TextLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'",
        ),
        "Outbound Flow": pdk.Layer(
            "ArcLayer",
            data=from_data_file("bart_path_stats.json"),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            auto_highlight=True,
            width_scale=0.0001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
    }
    st.sidebar.markdown("### Map Layers")
    selected_layers = [
        layer
        for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 37.76,
                    "longitude": -122.4,
                    "zoom": 11,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )

st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)


@st.cache
def get_UN_data():
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


try:
    df = get_UN_data()
    countries = st.multiselect(
        "Choose countries", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        st.write("### Gross Agricultural Production ($B)", data.sort_index())

        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )


source = pd.DataFrame({
    'symbol': ['GOOGLE', 'GOOGLE', 'AMAZON', 'AMAZON'],
    'date': [1, 2, 1, 2],
    'price': ['20', '25', '66', '64'],
})

def stock_gradient(symbol, color):
  return alt.Chart(source).transform_filter(
      f'datum.symbol==="{symbol}"'
  ).mark_area(
      line={'color': color},
      color=alt.Gradient(
          gradient='linear',
          stops=[alt.GradientStop(color='white', offset=0),
                alt.GradientStop(color=color, offset=1)],
          x1=1,
          x2=1,
          y1=1,
          y2=0
      )
  ).encode(
      alt.X('date:T'),
      alt.Y('price:Q')
  )

test = alt.layer(
    stock_gradient('GOOGLE', 'darkgreen'),
    stock_gradient('AMAZON', 'darkblue')
)

st.write(test)