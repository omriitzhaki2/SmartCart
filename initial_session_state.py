import streamlit as st
from utils import *


def initial():
    if 'name' not in st.session_state:
        st.session_state.name = ''

    if 'register' not in st.session_state:
        st.session_state.register = False

    if 'selected_supermarket' not in st.session_state:
        st.session_state.selected_supermarket = False

    if 'recommendation' not in st.session_state:
        st.session_state.recommendation = True

    if 'recommend_products_list' not in st.session_state:
        st.session_state.recommend_products_list = []

    if 'grocery' not in st.session_state:
        st.session_state.grocery = ''

    if 'closest_products' not in st.session_state:
        st.session_state.closest_products = []

    if 'shopping_list' not in st.session_state:
        st.session_state.shopping_list = []

    if 'selected_products' not in st.session_state:
        st.session_state.selected_products = []

    if 'selected_products_for_recipe' not in st.session_state:
        st.session_state.selected_products_for_recipe = False

    if 'selected_products_for_recipe1' not in st.session_state:
        st.session_state.selected_products_for_recipe1 = False

    if 'selected_meal_type' not in st.session_state:
        st.session_state.selected_meal_type = []

    if 'is_selected_meal_type' not in st.session_state:
        st.session_state.is_selected_meal_type = False

    if 'client' not in st.session_state:
        st.session_state.client = create_client_for_gpt()

    if 'user' not in st.session_state:
        st.session_state.user = None

    if 'supermarket_names' not in st.session_state:
        st.session_state.supermarket_names = {}

    if 'missing_dict1' not in st.session_state:
        st.session_state.missing_dict1 = {}

    if 'missing_dict2' not in st.session_state:
        st.session_state.missing_dict2 = {}

    if 'missing_dict3' not in st.session_state:
        st.session_state.missing_dict3 = {}

    if 'finish' not in st.session_state:
        st.session_state.finish = False

    if 'keren' not in st.session_state:
        st.session_state.keren = False

    if 'shortest_path' not in st.session_state:
        st.session_state.shortest_path = []

