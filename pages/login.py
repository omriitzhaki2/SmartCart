import streamlit as st
import json
from google.cloud import firestore
from utils import *
from layout.app_layout import *
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                   page_title="login",
                   page_icon=f'layout/logo.jpg')

# Custom function to create a centered title

st.markdown(set_title("Welcome to SmartCart"), unsafe_allow_html=True)
st.markdown(streamlit_style, unsafe_allow_html=True)
set_logo()
set_background(rf'layout/background.png')
set_button()

db = get_db_connection()


username = st.text_input('Enter your user name:')
password = st.text_input("Enter your password:", type="password")
button_clicked = st.button('Login')

if button_clicked:
    all_users = db.collection('users').get()
    incorrect_details = False
    for user in all_users:
        if user.get('username') == username:
            user_dict = db.collection('users').document(user.id).get().to_dict()
            if user_dict["password"] == password:
                st.session_state.name = user_dict["name"]
                st.session_state.user = db.collection('users').document(user.id)
                st.session_state.supermarket_names = st.session_state.user.get().to_dict()['nearest_supermarkets']
                switch_page('shopping_list')
                break

    incorrect_details = True
    if incorrect_details:
        st.markdown("""  
        <style>  
            .stAlert[data-st-id="warning"] {  
            }  
        </style>  
        """, unsafe_allow_html=True)
        st.warning("Incorrect username or password. Please try again.", icon="⚠️")

if st.button('Register'):
    switch_page('register')

if st.button('Home'):
    switch_page('home')



