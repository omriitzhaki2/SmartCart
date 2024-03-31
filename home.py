import streamlit as st
from layout.app_layout import *
from initial_session_state import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                   page_title="SmartCart",
                   page_icon=f'layout/logo.jpg')

set_button()
set_background(rf'layout/background.png')

st.session_state.clear()
initial()

st.markdown(streamlit_style, unsafe_allow_html=True)
st.markdown(set_title("Welcome to SmartCart"), unsafe_allow_html=True)
set_logo()

st.markdown(set_subtitle('List It Right, Shop It Light:'), unsafe_allow_html=True)
st.markdown(set_subsubtitle('Your Fast Track to Supermarket Solutions'), unsafe_allow_html=True)
st.markdown(set_text("""Simplify your supermarket experience with our smart shopping system!"""), unsafe_allow_html=True)
st.markdown(set_text("""Our system helps you create a comprehensive shopping list, </br>
            offers personalized recipes, tracks missing items,</br>
            and guides you through the store efficiently.</br>"""), unsafe_allow_html=True)
st.markdown(set_text('Say goodbye to wasted time and and enjoy a seamless shopping journey!'), unsafe_allow_html=True)

with st.expander("More Information..."):
    st.markdown(set_text('Our smart shopping system revolutionizes the way you shop by:'), unsafe_allow_html=True)
    st.markdown(set_text('Comprehensive Shopping Lists: Easily create and manage your shopping lists, with suggestions for similar products if an item is unavailable.'), unsafe_allow_html=True)
    st.markdown(set_text('Personalized Recipes: Input a food item or choose a cuisine, and get delicious recipes along with the ingredients needed.'), unsafe_allow_html=True)
    st.markdown(set_text('Efficient Shopping Routes: Receive a mapped-out route in the supermarket, optimized for the shortest path to collect all your items.'), unsafe_allow_html=True)
    st.markdown(set_text('Forgotten Item Recommendations: Get reminders for items you may have forgotten based on your preferences and past choices.'), unsafe_allow_html=True)
    st.markdown(set_text('Supermarket Recommendations: Discover the best supermarket to visit based on distance and item availability.'), unsafe_allow_html=True)
    st.markdown(set_text('User-Friendly Interface: Seamlessly navigate through the system, from logging in to receiving your customized shopping map.'), unsafe_allow_html=True)
    st.markdown(set_text('Convenient Email Notifications: Receive your personalized shopping map directly to your email for easy access.'), unsafe_allow_html=True)
    st.markdown(set_text('Experience the convenience, efficiency, and ease of our smart shopping system, designed to simplify your grocery trips and enhance your overall shopping experience. Say hello to stress-free shopping!'), unsafe_allow_html=True)


if st.button('Login'):
    switch_page("login")

if st.button('Register'):
    switch_page("register")

