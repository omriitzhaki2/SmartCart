import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from layout.app_layout import *
from utils import *
from PIL import Image
import io


st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                   page_title="super map",
                   page_icon=f'layout/logo.jpg')

st.markdown(set_title("SmartCart"), unsafe_allow_html=True)
st.markdown(streamlit_style, unsafe_allow_html=True)
set_logo()
set_background(rf'layout/background.png')
set_button()
set_download_button()

if st.session_state.user is None:
    st.error('You need to login or register')
    st.stop()


st.markdown(set_subsubtitle(f'Your Fast Supermarket Route to {st.session_state.supermarket}'), unsafe_allow_html=True)
products_list = st.session_state.shopping_list
if not st.session_state.finish:
    G = create_distance_products_graph(products_list)
    st.session_state.shortest_path = find_shortest_products_path_greedy(G)
    plot_shortest_path_on_map(st.session_state.shortest_path)
    st.session_state.finish = True
    st.session_state.shopping_list = []

col1, col2 = st.columns([3, 1])
with col1:
    st.image("layout/map.jpg")
with col2:
    st.markdown("### Grocery List:")
    for idx, (item, location) in enumerate(st.session_state.shortest_path, start=0):
        if item != 'start' and item != 'end':
            st.markdown(set_text(f"{idx}: {item}"), unsafe_allow_html=True)


# Save the image to a file
image = Image.open("layout/map.jpg")
img_bytes = io.BytesIO()
image.save(img_bytes, format="JPEG")
img_bytes.seek(0)

if st.download_button(label="Click to download the map",
                      data=img_bytes,
                      file_name="SuperMarket Map.jpg",
                      mime="image/jpeg",
                      key='download_image'):
    st.markdown(set_text('The map has been downloaded, enjoy the shopping!'), unsafe_allow_html=True)

if st.button('Return to home'):
    switch_page('home')
