import pandas as pd
import streamlit as st
import ast
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.stylable_container import stylable_container
from layout.app_layout import *
from utils import *


st.set_page_config(layout="centered",
                   initial_sidebar_state="collapsed",
                   page_title="shopping_list",
                   page_icon=f'layout/logo.jpg')

set_logo()
set_background(rf'layout/background.png')
set_button()


if st.session_state.user is None:
    st.error('You need to login or register')
    st.stop()


st.markdown(set_subsubtitle(f'Hello {st.session_state.name}!'), unsafe_allow_html=True)
st.markdown(set_text(f'Good to see you again'), unsafe_allow_html=True)


def update_shopping_list():
    st.markdown(set_text(''), unsafe_allow_html=True)
    st.markdown(set_subtitle('🍒 My Shopping List: 🍒'), unsafe_allow_html=True)
    st.markdown(set_text(''), unsafe_allow_html=True)
    st.session_state.shopping_list = list(set(st.session_state.shopping_list))
    for item in st.session_state.shopping_list:
        col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
        with col1:
            st.markdown(set_text('🛒'), unsafe_allow_html=True)
        with col2:
            st.markdown(set_text_list(f"{item}", color='#2F2559'), unsafe_allow_html=True)
        with col3:
            with stylable_container(
                    "home1",
                    css_styles=set_custom_button(),
            ):
                if st.button("Remove 🗑", key=f'remove_{item}'):
                    st.session_state.shopping_list.remove(item)
                    st.experimental_rerun()
        with col4:
            st.markdown(set_text('🛒', text_align='left'), unsafe_allow_html=True)


st.markdown(set_text(''), unsafe_allow_html=True)
st.markdown(set_text('Click on each subpage to learn more about its functionality', 'left'), unsafe_allow_html=True)

products_list = get_products_list()
tab1, tab2, tab3 = st.tabs(["Find Products", "Get Recipes", "Discover Cuisines"])
with tab1:
    st.markdown(set_text('❓ Enter any product name and receive suggestions for similar items '
                         'available in the supermarket.', 'left'), unsafe_allow_html=True)
    st.markdown(set_text('Then, add selected items to your shopping list.', 'left'), unsafe_allow_html=True)
    st.markdown('<style>input[type="text"] { font-size: 20px; }</style>', unsafe_allow_html=True)
    st.markdown(set_text('\nEnter Grocery:', 'left'), unsafe_allow_html=True)
    grocery = st.text_input('', value='', key='Enter Grocery:' , label_visibility='collapsed')
    if grocery != '' and len(st.session_state.closest_products) == 0:
        if st.session_state.grocery != grocery:
            st.session_state.closest_products = find_closest_matches([grocery], products_list)[grocery]
            st.session_state.grocery = grocery
            st.session_state.missing_dict1 = check_products_inventory_per_product(st.session_state.closest_products,
                                                                                 st.session_state.supermarket_names,
                                                                                 mode='table')


    if len(st.session_state.closest_products) > 0:
        choose_product = st.empty()
        products_list_selection = st.empty()
        choose_product.markdown(set_text('Choose your product: ', 'left'), unsafe_allow_html=True)
        products_list_selection = st.empty()
        chosen_product = products_list_selection.radio('', st.session_state.closest_products, label_visibility='collapsed')
        check_availability_text = st.empty()
        check_availability_text1 = st.empty()
        check_availability_text.markdown(set_text(f'\n', 'left'),
                                         unsafe_allow_html=True)
        check_availability_text1.markdown(set_text(f'\nAvailability of {chosen_product}:', 'left'), unsafe_allow_html=True)
        df = pd.DataFrame(st.session_state.missing_dict1).T
        df = df.map(
            lambda x: f'<div style="color:#03AC13;text-align: center;font-weight: bold;">✔</div>' if int(
                x) > 0 else f'<div style="text-align: center;">❌</div>')
        check_availability = st.empty()
        check_availability.write(df.T[[chosen_product]].T.to_html(escape=False), unsafe_allow_html=True)
        add_to_shopping_list_button = st.empty()
        if add_to_shopping_list_button.button('Add to shopping list', key='Add to shopping list1'):
            st.markdown(set_text('The item was added to your cart'), unsafe_allow_html=True)
            st.session_state.closest_products = []
            st.session_state.shopping_list.append(chosen_product)
            products_list_selection.empty()
            choose_product.empty()
            add_to_shopping_list_button.empty()
            check_availability_text = st.empty()
            check_availability.empty()
            check_availability_text.empty()
            check_availability_text1.empty()


with tab2:
    st.markdown(set_text('❓ Enter a dish name to get its recipe and a list of ingredients '
                         'available in the supermarket.', 'left'), unsafe_allow_html=True)
    st.markdown(set_text('Then, add selected items to your shopping list.', 'left'), unsafe_allow_html=True)
    st.markdown('<style>input[type="text"] { font-size: 20px; }</style>', unsafe_allow_html=True)
    st.markdown(set_text('\n Enter a dish:', 'left'), unsafe_allow_html=True)
    dish = st.text_input('', key='Enter a dish:', label_visibility='collapsed')
    if st.button(f'Find recipe and groceries', key='Find recipe'):
        try:
            dish_dict = get_response(st.session_state.client, dish, "RECIPE")
            st.session_state.selected_products_for_recipe = True
            closest_products_dict = find_closest_matches(dish_dict['products'], products_list)
            dict_products_for_query = {'meal name': dish,
                                       'recipe': dish_dict['recipe'],
                                       'products': closest_products_dict
                                       }
            products_dict = get_response(st.session_state.client, str(dict_products_for_query), "MATCH")
            st.session_state.selected_products = [list(products_dict.values()), dish_dict['recipe']]
            st.session_state.missing_dict2 = check_products_inventory_per_product(st.session_state.selected_products[0],
                                                                                 st.session_state.supermarket_names,
                                                                                 mode='table')
        except:
            st.error('I apologize for the inconvenience, Can you press the button again?')
    if st.session_state.selected_products_for_recipe:
        products = st.session_state.selected_products[0]
        recipe = st.session_state.selected_products[1]
        place_holder1 = st.empty()
        place_holder2 = st.empty()
        place_holder3 = st.empty()
        place_holder4 = st.empty()
        place_holder5 = st.empty()
        place_holder6 = st.empty()
        place_holder1.markdown(set_subtitle('The Recipe:'), unsafe_allow_html=True)
        place_holder2.markdown(set_text_with_dots(recipe), unsafe_allow_html=True)
        place_holder3.markdown(set_subtitle('The Groceries:'), unsafe_allow_html=True)
        place_holder4.markdown(set_text('Select products:', 'left'), unsafe_allow_html=True)
        selected_products = place_holder5.multiselect('', options=products, default=products, label_visibility='collapsed')
        with place_holder6.expander("Check availability of the products..."):
            df = pd.DataFrame(st.session_state.missing_dict2).T
            df = df.map(lambda x: f'<div style="color:#03AC13;text-align: center;font-weight: bold;">✔</div>' if int(x) > 0 else f'<div style="text-align: center;">❌</div>')
            st.write(df.to_html(escape=False), unsafe_allow_html=True)
        if st.button('Add to shopping list', key='Add to shopping list2'):
            st.markdown(set_text('The items were added to your cart'), unsafe_allow_html=True)
            for product in selected_products:
                st.session_state.shopping_list.append(product)
            st.session_state.selected_products = []
            st.session_state.selected_products_for_recipe = False
            place_holder1.empty()
            place_holder2.empty()
            place_holder3.empty()
            place_holder4.empty()
            place_holder5.empty()
            place_holder6.empty()

with tab3:
    st.markdown(set_text('❓ Choose a cuisine and discover 10 popular dishes.', 'left'), unsafe_allow_html=True)
    st.markdown(set_text('Select a dish to view its recipe and add ingredients to your shopping '
                         'list.', 'left'), unsafe_allow_html=True)
    course_meals = ['Italian', 'American', 'Mexican', 'Chinese', 'Japanese', 'Indian', 'French', 'Greek', 'Thai',
                    'Spanish', 'Mediterranean', 'Vietnamese', 'Korean', 'Middle Eastern', 'Israeli']

    st.markdown(set_subsubtitle('Choose your favorite meal type:', 'left'), unsafe_allow_html=True)
    favorite_food_type = st.selectbox("", course_meals, label_visibility='collapsed')
    if st.button(f'Show Me {favorite_food_type} Meals ', key='Show Me'):
        try:
            st.session_state.selected_meal_type = get_response(st.session_state.client, favorite_food_type, "COURSE")
            st.session_state.is_selected_meal_type = True
            st.session_state.selected_products_for_recipe1 = False
        except:
            st.error('I apologize for the inconvenience, Can you press the button again?')
    if st.session_state.is_selected_meal_type:
        meal_list = [f"**{meal.split(': ', 1)[0]}**" for meal in st.session_state.selected_meal_type]
        description_list = [f"{meal.split(': ', 1)[-1]}" for meal in st.session_state.selected_meal_type]
        st.markdown(set_subsubtitle('Select a Meal:', 'left'), unsafe_allow_html=True)
        selected_meal_name = st.radio("", options=meal_list, captions=description_list, label_visibility='collapsed')
        dish = [meal for meal in st.session_state.selected_meal_type if selected_meal_name[2:-2] in meal][0]
        if st.button(f'Find recipe and groceries', key='Find recipe2'):
            try:
                dish_dict = get_response(st.session_state.client, dish, "RECIPE")
                st.session_state.selected_products_for_recipe1 = True
                closest_products_dict = find_closest_matches(dish_dict['products'], products_list)
                dict_products_for_query = {'meal name': dish,
                                           'recipe': dish_dict['recipe'],
                                           'products': closest_products_dict
                                           }
                products_dict = get_response(st.session_state.client, str(dict_products_for_query), "MATCH")
                st.session_state.selected_products = [list(products_dict.values()), dish_dict['recipe']]
                st.session_state.missing_dict3 = check_products_inventory_per_product(
                    st.session_state.selected_products[0],
                    st.session_state.supermarket_names,
                    mode='table')
            except:
                st.error('I apologize for the inconvenience, Can you press the button again?')
    if st.session_state.selected_products_for_recipe1:
        products = st.session_state.selected_products[0]
        recipe = st.session_state.selected_products[1]
        place_holder1 = st.empty()
        place_holder2 = st.empty()
        place_holder3 = st.empty()
        place_holder4 = st.empty()
        place_holder5 = st.empty()
        place_holder6 = st.empty()
        place_holder7 = st.empty()
        place_holder1.markdown(set_subtitle('The Recipe:'), unsafe_allow_html=True)
        place_holder2.markdown(set_text_with_dots(recipe), unsafe_allow_html=True)
        place_holder3.markdown(set_subtitle('The Groceries:'), unsafe_allow_html=True)
        place_holder5.markdown(set_text('Select products:', 'left'), unsafe_allow_html=True)
        selected_products = place_holder6.multiselect('', options=products, default=products, label_visibility='collapsed')
        with place_holder7.expander("Check availability of the products..."):
            df = pd.DataFrame(st.session_state.missing_dict3).T
            df = df.map(
                lambda x: f'<div style="color:#03AC13;text-align: center;font-weight: bold;">✔</div>' if int(
                    x) > 0 else f'<div style="text-align: center;">❌</div>')
            st.write(df.to_html(escape=False), unsafe_allow_html=True)
        if st.button('Add to shopping list', key='Add to shopping list3'):

            st.markdown(set_text('The items were added to your cart'), unsafe_allow_html=True)
            for product in selected_products:
                st.session_state.shopping_list.append(product)
            st.session_state.selected_products = []
            st.session_state.selected_products_for_recipe1 = False
            place_holder1.empty()
            place_holder2.empty()
            place_holder3.empty()
            place_holder4.empty()
            place_holder5.empty()
            place_holder6.empty()
            place_holder7.empty()


if len(st.session_state.shopping_list) > 0:
    update_shopping_list()

    if st.button('Finish Shopping List'):
        switch_page('recommendations')
