import pickle
import json
import ast
import time


import pandas as pd
import numpy as np
import networkx as nx
import streamlit as st
from collections import Counter

import matplotlib.pyplot as plt
from itertools import permutations
from PIL import Image, ImageDraw, ImageFont
from google.cloud import firestore
from fuzzywuzzy import process
import openai
from serpapi import GoogleSearch

# pip install google-search-results


# FIREBASE_KEY = 'AIzaSyAGttqzfQT-I6ZK7SXmsS-nT-_PLftkDw0'
PRODUCTS_PATH = 'data/final_products_supermarket.csv'
MAP_GRAPH_PATH = 'data/map_graph.pkl'
MAP_PATH = 'layout/supermarket_map.jpg'
START_NODE = ('start', (981, 510))
END_NODE = ('end', (398, 510))


@st.cache_resource
def get_db_connection():
    with open('config.json', 'r') as file:
        config = json.load(file)
    FIREBASE_JSON = st.secrets['FIREBASE_JSON']
    db = firestore.Client.from_service_account_json(FIREBASE_JSON)
    return db


def get_GPS_location(city, street):
    with open('config.json', 'r') as file:
        config = json.load(file)
    api_key = st.secrets['GOOGLE_API']
    params = {
        "engine": "google_maps",
        "q": f"{street} street, {city}",
        "type": "search",
        "api_key": api_key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results['place_results']['gps_coordinates']



def create_client_for_gpt():
    with open('config.json', 'r') as file:
        config = json.load(file)

    OPENAI_KEY = st.secrets['OPENAI_KEY']
    openai.api_key = OPENAI_KEY
    client = openai.OpenAI(api_key=OPENAI_KEY)
    return client


def get_response(client, prompt, assignment_type):
    with open('config.json', 'r') as file:
        assignment = json.load(file)['ASSIGNMENTS']

    your_assignment = assignment[assignment_type]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": your_assignment},
          {"role": "user", "content": prompt}
        ]
      )
    print(completion.choices[0].message.content)
    return ast.literal_eval(completion.choices[0].message.content)


def find_closest_matches(user_inputs, products_list, num_matches=15):
    closest_matches = {}
    for user_input in user_inputs:
        matches = process.extract(user_input, products_list, limit=num_matches)
        closest_matches[user_input] = [match for match, score in matches]
    return closest_matches


def get_products_list():
    product_df = pd.read_csv(PRODUCTS_PATH)
    return list(product_df['product_name'])


def check_products_inventory(products_list):
    df = pd.read_csv(PRODUCTS_PATH)
    missing_inventory_dict = {'super1': [],
                              'super2': [],
                              'super3': [],
                              }
    for product in products_list:
        product_df = df[df['product_name'] == product]
        for i in range(1,4):
            product_inventory = product_df[f'product_inventory_super{i}'].iloc[0]
            if product_inventory == 0:
                missing_inventory_dict[f'super{i}'].append(product)

    # Find the super with the minimum length
    best_super = min(missing_inventory_dict, key=lambda k: len(missing_inventory_dict[k]))

    return missing_inventory_dict, best_super


def check_products_inventory_per_product(products_list, supermarket_names, mode='list'):
    df = pd.read_csv(PRODUCTS_PATH)
    if mode == 'list':
        missing_inventory_list = []
        for product in products_list:
            product_df = df[df['product_name'] == product]
            product_inventory_list = []
            for i in range(1, 4):
                product_inventory = product_df[f'product_inventory_super{i}'].iloc[0]
                if product_inventory == 0:
                    product_inventory_list.append(supermarket_names[f'super{i}'])
            if len(product_inventory_list) == 0:
                missing_inventory_list.append('This product is available in all supermarkets')
            elif len(product_inventory_list) == 3:
                missing_inventory_list.append(f"This product is missing in all supermarkets")
            else:
                missing_inventory_list.append(f"This product is missing in: {', '.join(product_inventory_list)}")
        return missing_inventory_list
    else:
        missing_inventory_dict = {}
        for product in products_list:
            product_df = df[df['product_name'] == product]
            missing_inventory_dict[product] = {}
            for i in range(1, 4):
                product_inventory = product_df[f'product_inventory_super{i}'].iloc[0]
                if product_inventory == 0:
                    missing_inventory_dict[product][supermarket_names[f'super{i}']] = 0
                else:
                    missing_inventory_dict[product][supermarket_names[f'super{i}']] = 1
        return missing_inventory_dict



def calculate_time_difference(current_time, previous_time):
    # Function to calculate the time difference between two timestamps
    return (current_time - previous_time) / (60 * 60 * 24 * 7)


def recommend_products(current_shopping_list, previous_shopping_lists, num_recommendations=5):
    # Function to recommend products based on similar shopping lists and time difference
    current_shopping_set = set(current_shopping_list['items'])
    current_time = current_shopping_list['time']
    time_differences = [calculate_time_difference(current_time, prev['time']) for prev in previous_shopping_lists]

    product_counts = Counter()
    for prev, time_diff in zip(previous_shopping_lists, time_differences):
        prev_items = set(prev['items'])
        # weight products based on the time difference
        weight_factor = 1 / (time_diff + 1)
        # Update product counts considering time difference
        for item in prev_items:
            product_counts[item] += weight_factor

    # Remove products already in the current shopping list
    for item in current_shopping_set:
        if item in product_counts:
            del product_counts[item]

    # Get top recommended products based on occurrence frequency
    recommended_products = [product for product, _ in product_counts.most_common(num_recommendations)]
    return recommended_products


def sample_products_by_department(products_list, num_samples=3):
    df = pd.read_csv(PRODUCTS_PATH)

    product_df = df[df['product_name'].isin(products_list)]
    department_counts = product_df['department'].value_counts()
    most_common_department = department_counts.idxmax()

    department_products = df[(df['department'] == most_common_department) & (~df['product_name'].isin(products_list))]
    sampled_products = department_products.sample(n=num_samples)['product_name'].tolist()
    return sampled_products


def recommendation_system(previous_shopping_lists, current_shopping_list):
    recommended_products_list = sample_products_by_department(current_shopping_list['items'], num_samples=3)
    if len(previous_shopping_lists) > 0:
        recommended_products_list += recommend_products(current_shopping_list, previous_shopping_lists)

    return recommended_products_list


def create_distance_products_graph(products_list):
    with open(MAP_GRAPH_PATH, 'rb') as f:
        map_graph = pickle.load(f)
    products_df = pd.read_csv(PRODUCTS_PATH)

    # Create a new graph for the shopping list
    shopping_graph = nx.Graph()

    # Add nodes to the shopping graph for each product in the shopping list
    shopping_graph.add_node(START_NODE)
    shopping_graph.add_node(END_NODE)
    for product in products_list:
        # Get the coordinates of the product from the DataFrame
        y = products_df[products_df['product_name'] == product]['x_closest_location'].iloc[0]
        x = products_df[products_df['product_name'] == product]['y_closest_location'].iloc[0]
        shopping_graph.add_node((product, (x, y)))

    nodes_list = list(shopping_graph.nodes())
    for node_u in shopping_graph.nodes():
        u, coord_u = node_u
        nodes_list.remove(node_u)
        for node_v in nodes_list:
            v, coord_v = node_v
            if u != v:
                shortest_path_len = nx.shortest_path_length(map_graph, source=coord_u, target=coord_v)
                shopping_graph.add_edge(node_u, node_v, weight=shortest_path_len)
                shopping_graph.add_edge(node_v, node_u, weight=shortest_path_len)

    return shopping_graph


def find_shortest_products_path(shopping_graph):
    # Get all internal nodes (excluding start and end nodes)
    internal_nodes = [node for node in shopping_graph.nodes() if node not in [START_NODE, END_NODE]]
    # Generate permutations of internal nodes only
    internal_permutations = permutations(internal_nodes)

    # Calculate the length of each path
    shortest_length = float('inf')
    shortest_path = None
    for perm in internal_permutations:
        length = shopping_graph[START_NODE][perm[0]]['weight']
        length += sum(shopping_graph[perm[i]][perm[i + 1]]['weight'] for i in range(len(perm) - 1))
        length += shopping_graph[perm[-1]][END_NODE]['weight']
        if length < shortest_length:
            shortest_length = length
            shortest_path = (START_NODE, ) + perm + (END_NODE, )
    return shortest_path


def find_shortest_products_path_greedy(shopping_graph, maximum_permutations=10):
    number_of_products_to_greedy_mode = shopping_graph.number_of_nodes() - maximum_permutations - 2
    visited_products = [START_NODE, END_NODE]
    greedy_shortest_path = (START_NODE, )

    prev_node = START_NODE
    next_node = START_NODE
    node_list = list(shopping_graph.nodes())
    node_list.remove(START_NODE)
    node_list.remove(END_NODE)
    for i in range(number_of_products_to_greedy_mode):
        min_weight = float('inf')
        for node in node_list:
            weight = shopping_graph[prev_node][node]['weight']
            if weight < min_weight:
                next_node = node
                min_weight = weight

        prev_node = next_node
        node_list.remove(next_node)
        visited_products.append(next_node)
        greedy_shortest_path += (next_node, )

    # Get all internal nodes (excluding start and end nodes)
    internal_nodes = [node for node in shopping_graph.nodes() if node not in visited_products]
    # Generate permutations of internal nodes only
    internal_permutations = permutations(internal_nodes)

    # Calculate the length of each path
    shortest_length = float('inf')
    shortest_path = None
    for perm in internal_permutations:
        length = shopping_graph[prev_node][perm[0]]['weight']
        length += sum(shopping_graph[perm[i]][perm[i + 1]]['weight'] for i in range(len(perm) - 1))
        length += shopping_graph[perm[-1]][END_NODE]['weight']
        if length < shortest_length:
            shortest_length = length
            shortest_path = greedy_shortest_path + perm + (END_NODE, )
    return shortest_path


def plot_shortest_path_on_map(shortest_path):
    with open(MAP_GRAPH_PATH, 'rb') as f:
        map_graph = pickle.load(f)
    # Load your PNG map using PIL
    png_map = Image.open(MAP_PATH)
    draw = ImageDraw.Draw(png_map)

    walk_coordinates = []
    for index in range(len(shortest_path)-1):
        walk_coordinates += nx.shortest_path(map_graph, source=shortest_path[index][1], target=shortest_path[index+1][1])
        walk_coordinates += nx.shortest_path(map_graph, source=shortest_path[index][1],
                                             target=shortest_path[index + 1][1])

    font = ImageFont.load_default().font_variant(size=20)
    for i, coord in enumerate(walk_coordinates):
        if i % 10 == 0:
            x_coord, y_coord = coord
            draw.text((y_coord, x_coord), str('•'), fill='black', font=font)

    products_df = pd.read_csv(PRODUCTS_PATH)
    for idx, node in enumerate(shortest_path, start=0):
        # Find the node in the DataFrame
        if node[0] == 'start' or node[0] == 'end':
            continue
        node_data = products_df[products_df['product_name'] == node[0]]
        x_loc = node_data['x_location'].iloc[0]
        y_loc = node_data['y_location'].iloc[0]

        # Draw the number on the PNG map at the specified location
        circle_radius = 17
        circle_coords = (x_loc+5 - circle_radius, y_loc+10 - circle_radius, x_loc+5 + circle_radius, y_loc+10 + circle_radius)
        draw.ellipse(circle_coords, fill='white', outline='black')  # Adjust outline color as needed
        if idx > 9:
            x_loc -= 7
        y_loc -= 2

        draw.text((x_loc, y_loc), str(idx), fill='black', font=font)

    png_map.save('layout/map.jpg')
