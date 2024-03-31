import streamlit as st
from datetime import datetime
import time
from utils import *
from layout.app_layout import *
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                   page_title="recommendations",
                   page_icon=f'layout/logo.jpg')
st.markdown(set_title("SmartCart"), unsafe_allow_html=True)
st.markdown(streamlit_style, unsafe_allow_html=True)
set_logo()
set_background(rf'layout/background.png')
set_button()


if st.session_state.user is None:
    st.error('You need to login or register')
    st.stop()

st.markdown(set_subtitle("Recommendations", 'left'), unsafe_allow_html=True)
st.markdown(set_text('Products you may have forgotten:', 'left'), unsafe_allow_html=True)

# st.session_state.recommendation = True
previous_shopping_lists = st.session_state.user.get().to_dict()['history']
current_shopping_list = {'time': int(time.time()), 'items': list(st.session_state.shopping_list)}
if st.session_state.recommendation:
    st.session_state.recommend_products_list = recommendation_system(previous_shopping_lists, current_shopping_list)
    st.session_state.recommendation = False


selected_products = st.multiselect('', options=st.session_state.recommend_products_list, placeholder="Choose products", label_visibility='collapsed')
if st.button('Add to shopping list', key='omri'):
    st.markdown(set_text('The items were added to your cart'), unsafe_allow_html=True)
    for product in selected_products:
        st.session_state.shopping_list.append(product)

st.markdown(set_subsubtitle('🛒 Your final shopping list: 🛒'), unsafe_allow_html=True)
shopping_list = st.session_state.shopping_list
shopping_list_text = "<br>".join(shopping_list)
st.markdown(set_text(shopping_list_text), unsafe_allow_html=True)

supermarket_names = st.session_state.user.get().to_dict()['nearest_supermarkets']

if len(st.session_state.shopping_list) > 0:
    temp = st.empty()
    if temp.button('Update Shopping List'):
        st.session_state.keren = not st.session_state.keren
        temp.empty()

    if st.session_state.keren:
        temp.empty()
        update_list = st.multiselect('', options=st.session_state.shopping_list, default=st.session_state.shopping_list,
                                         label_visibility='collapsed')
        if st.button('Finish Updating'):
            st.session_state.shopping_list = update_list
            st.session_state.keren = not st.session_state.keren
            st.experimental_rerun()

if st.button('Continue Shopping'):
    switch_page('shopping_list')

if st.button('Finish Shopping List'):
    st.session_state.selected_supermarket = True

if st.session_state.selected_supermarket:
    missing_dict, best_super = check_products_inventory(st.session_state.shopping_list)
    st.markdown(set_subsubtitle("Choose SuperMarket", 'left'), unsafe_allow_html=True)
    supermarket_options = [f"**{supermarket_names['super1']}**",
                           f"**{supermarket_names['super2']}**",
                           f"**{supermarket_names['super3']}**"]
    missing_products = [f"**missing {len(missing_dict['super1'])} products:** {', '.join(missing_dict['super1'])}",
                        f"**missing {len(missing_dict['super2'])} products:** {', '.join(missing_dict['super2'])}",
                        f"**missing {len(missing_dict['super3'])} products:** {', '.join(missing_dict['super3'])}"]

    supermarket = st.radio('', supermarket_options, captions=missing_products, label_visibility='collapsed')
    st.markdown(set_text(f"We recommend you to go to {supermarket_names[best_super]}"), unsafe_allow_html=True)
    st.session_state.supermarket = supermarket[2:-2]

    if st.button('Get best shopping route'):
        super_key = [key for key, val in supermarket_names.items() if val == st.session_state.supermarket][0]
        for product in missing_dict[super_key]:
            st.session_state.shopping_list.remove(product)
        st.session_state.user.update({"history": previous_shopping_lists + [current_shopping_list]})
        switch_page('supermarket_map')
