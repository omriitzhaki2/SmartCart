import streamlit as st
from layout.app_layout import *
from initial_session_state import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_modal import Modal


st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                   page_title="SmartCart",
                   page_icon=f'layout/logo.jpg')

set_button()
set_background(rf'layout/background.png')

st.session_state.clear()
initial()

set_logo()

st.markdown(set_subtitle('List It Right, Shop It Light:'), unsafe_allow_html=True)
st.markdown(set_subsubtitle('Your Fast Track to Supermarket Solutions'), unsafe_allow_html=True)
st.markdown(set_text("""Simplify your supermarket experience with our smart shopping system!"""), unsafe_allow_html=True)
st.markdown(set_text("""Our system helps you create a comprehensive shopping list, </br>
            offers personalized recipes, tracks missing items,</br>
            and guides you through the store efficiently.</br>"""), unsafe_allow_html=True)
st.markdown(set_text('Say goodbye to wasted time and and enjoy a seamless shopping journey!'), unsafe_allow_html=True)
st.image('layout/cart.jpg')

modal = Modal(key="Demo Key", title='')
open_modal = st.button(label='More Information...')
if open_modal:
    with modal.container():
        popup_content = """
                    <div class="popup" id="popup">
                        <h2 style="text-align: center;font-family: Trebuchet MS;color: #20115E;'">Our smart shopping system:</h2>
                        <ul>
                            <div style="line-height: 1.8;">🛒 Easily create and manage your shopping lists, with suggestions for similar products if an item is unavailable.<br></div>
                            <div style="line-height: 1.8;">🛒 Input a food item or choose a cuisine, and get delicious recipes along with the ingredients needed.<br></div>
                            <div style="line-height: 1.8;">🛒 Receive a mapped-out route in the supermarket, optimized for the shortest path to collect all your items.<br></div>
                            <div style="line-height: 1.8;">🛒 Get reminders for items you may have forgotten based on your preferences and past choices.<br></div>
                            <div style="line-height: 1.8;">🛒 Discover the best supermarket to visit based on distance and item availability.<br></div>
                            <div style="line-height: 1.8;">🛒 Seamlessly navigate through the system, from logging in to receiving your customized shopping map.<br></div>
                            <div style="line-height: 1.8;">🛒 Receive your personalized shopping map directly to your email for easy access.<br></div>
                             <div style="text-align: center;"><br> Say hello to stress-free shopping!<br></div>
                        </ul>                    
                    </div>

                """
        st.markdown(popup_content, unsafe_allow_html=True)
        close_modal = st.button(label='Close')

        if close_modal:
            modal.close()

# if st.button("More Information..."):
#     st.markdown(
#         """
#         <style>
#         .popup {
#             position: fixed;
#             top: 40%;
#             left: 50%;
#             transform: translate(-30%, -5%);
#             background-color: white;
#             padding: 10px;
#             border: 4px solid #20115E;
#             z-index: 1000;
#             font-family: Trebuchet MS;
#         }
#         </style>
#         """
#         , unsafe_allow_html=True)
#
#     st.markdown(
#         """
#         <script>
#         function closePopup() {
#             var popup = document.querySelector('.popup');
#             popup.parentNode.removeChild(popup);
#         }
#         </script>
#         """,
#         unsafe_allow_html=True
#     )
#     st.markdown(
#         """
#         <script>
#         function closePopup() {
#             var popup = document.querySelector('.popup');
#             popup.parentNode.removeChild(popup);
#         }
#         </script>
#         """,
#         unsafe_allow_html=True
#     )
#
#     popup_content = """
#             <div class="popup" id="popup">
#                 <h2 style="text-align: center;font-family: Trebuchet MS;color: #20115E;'">Our smart shopping system:</h2>
#                 <ul>
#                     <div style="line-height: 1.8;">🛒 Easily create and manage your shopping lists, with suggestions for similar products if an item is unavailable.<br></div>
#                     <div style="line-height: 1.8;">🛒 Input a food item or choose a cuisine, and get delicious recipes along with the ingredients needed.<br></div>
#                     <div style="line-height: 1.8;">🛒 Receive a mapped-out route in the supermarket, optimized for the shortest path to collect all your items.<br></div>
#                     <div style="line-height: 1.8;">🛒 Get reminders for items you may have forgotten based on your preferences and past choices.<br></div>
#                     <div style="line-height: 1.8;">🛒 Discover the best supermarket to visit based on distance and item availability.<br></div>
#                     <div style="line-height: 1.8;">🛒 Seamlessly navigate through the system, from logging in to receiving your customized shopping map.<br></div>
#                     <div style="line-height: 1.8;">🛒 Receive your personalized shopping map directly to your email for easy access.<br></div>
#                      <div style="text-align: center;"><br> Say hello to stress-free shopping!<br></div>
#                 </ul>
#                 <br>
#                 <button onclick="closePopup()">Close</button>
#             </div>
#
#         """
#     st.markdown(popup_content, unsafe_allow_html=True)
#
#     st.markdown(
#         """
#         <script>
#         function closePopup() {
#             ;l';l;'l
#         }
#         </script>
#         """,
#         unsafe_allow_html=True
#     )
#
#     if st.button("Close More Information"):
#         st.markdown(
#             """
#             <script>
#             var popup = document.querySelector('.popup');
#             popup.parentNode.removeChild(popup);
#             </script>
#             """,
#             unsafe_allow_html=True
#         )

if st.button('Login'):
    switch_page("login")

if st.button('Register'):
    switch_page("register")

