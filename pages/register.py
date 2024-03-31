import streamlit as st
import pandas as pd
from layout.app_layout import *
from geopy.distance import geodesic
from streamlit_extras.switch_page_button import switch_page
from utils import *


st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                   page_title="register",
                   page_icon=f'layout/logo.jpg')

st.markdown(set_title("Welcome to SmartCart"), unsafe_allow_html=True)
st.markdown(streamlit_style, unsafe_allow_html=True)
set_logo()
set_background(rf'layout/background.png')
set_button()
db = get_db_connection()


# Interactive Widgets for Registration Page
name = st.text_input("Enter your name:")
new_username = st.text_input('Enter a new user name:')
new_password = st.text_input("Enter a new password", type="password")
email = st.text_input("Enter your email:")
col1, col2 = st.columns(2)
with col1:
    city = st.text_input("Enter your city name:")
with col2:
    street = st.text_input("Enter your street name:")

if st.button('Register'):
    st.session_state.register = True
    # Define the document data for the new user
    user_data = {
        'name': name,
        'username': new_username,
        'password': new_password,
        'email': email,
        'city': city,
        'street': street,
        'history': [],
        'nearest_supermarkets': {"super1": "Technion SuperMarket",
                                 "super2": "Mercaz HaCarmel SuperMarket",
                                 "super3": "Haifa Port SuperMarket"
                                }
    }
    # Add the new user data to the 'users' collection
    db.collection('users').add(user_data)

if st.button('Home'):
    switch_page('home')

if st.session_state.register:
    st.markdown(set_subsubtitle('Nearest SuperMarkets'), unsafe_allow_html=True)
    st.markdown(set_text('Your location in blue, Nearest supermarkets in red'), unsafe_allow_html=True)
    # List of shop locations (replace with your desired shop coordinates)
    supermarket_locations = {
        "Technion SuperMarket": (32.7775, 35.0214),
        "Mercaz HaCarmel SuperMarket": (32.8055, 34.9891),
        "Haifa Port SuperMarket": (32.8193, 34.9885)}

    user_location = get_GPS_location(city, street)
    user_location = (user_location['latitude'], user_location['longitude'])
    # Supermarket locations in Haifa
    haifa_supermarkets = {
        "lat": [32.775, 32.8193, 32.8055, user_location[0]],
        "lon": [35.0214, 34.9885, 34.9891, user_location[1]],
        'color': ['#FF0000', '#FF0000', '#FF0000', '#0000FF'],
    }

    df = pd.DataFrame(haifa_supermarkets)
    distances = {name: geodesic(user_location, coord).kilometers for name, coord in supermarket_locations.items()}
    sorted_supermarkets = sorted(supermarket_locations.items(), key=lambda x: distances[x[0]])
    st.markdown(set_text(f'Closest Supermarket: {sorted_supermarkets[0][0]}'), unsafe_allow_html=True)
    map_data = st.map(df, color='color', zoom=12)
    if st.button('Login'):
        st.session_state.register = False
        switch_page('login')






