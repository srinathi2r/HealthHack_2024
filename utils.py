#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:52:46 2024

@author: srinath
"""

import streamlit as st
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def local_css(file_name):
    """
    Injects custom CSS styles into the Streamlit app.
    Args:
    file_name (str): The file name of the CSS file.
    """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        

def generate_mock_transaction_data(locations, products, max_count=20):
    """
    Generates mock transaction data for illustration purposes.
    Args:
    locations (list): List of locations.
    products (list): List of product names.
    max_count (int): Maximum number of transactions for a product at a location.
    Returns:
    DataFrame: A DataFrame with simulated transaction data.
    """
    data = []
    for location in locations:
        for product in products:
            buy_count = random.randint(0, max_count)
            sell_count = random.randint(0, max_count)
            data.append([location, product, buy_count, sell_count])
    return pd.DataFrame(data, columns=["Location", "Product", "Buy Count", "Sell Count"])

def find_most_frequent_items(df):
    """
    Finds the most frequently bought and sold items for each location.
    Args:
    df (DataFrame): DataFrame containing transaction data.
    Returns:
    DataFrame: A DataFrame with the most frequent buy and sell for each location.
    """
    most_frequent = df.groupby(['Location', 'Product']).sum()
    most_frequent = most_frequent.sort_values(['Location', 'Buy Count', 'Sell Count'], ascending=False).reset_index()
    most_frequent = most_frequent.drop_duplicates(subset='Location', keep='first')
    return most_frequent[['Location', 'Product', 'Buy Count', 'Sell Count']]


def plot_most_frequent_transactions(df):
    """
    Plots the most frequently bought and sold items for each location.
    Args:
    df (DataFrame): DataFrame containing the most frequent items data.
    """
    print(df['Location'].value_counts())
    fig, ax = plt.subplots(figsize=(10, 6))

    # Bar plot for each location
    locations = df['Location'].unique()
    n_bars = len(locations) * 2  # Two bars (buy and sell) per location
    bar_width = 0.35
    index = np.arange(0, n_bars, 2)  # Space out the locations

    for i, loc in enumerate(locations):
        loc_data = df[df['Location'] == loc]
        ax.bar(index[i], loc_data['Buy Count'].values[0], width=bar_width, color='orange', label='Buy' if i == 0 else "")
        ax.bar(index[i] + bar_width, loc_data['Sell Count'].values[0], width=bar_width, color='gray', label='Sell' if i == 0 else "")

    ax.set_xlabel('Department and Transaction Type')
    ax.set_ylabel('Transaction Count')
    
    # Set the position of the x-ticks
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels([f'{loc} - Buy/Sell' for loc in locations])

    ax.legend(loc='upper right')
    plt.xticks(rotation=45)
    st.pyplot(fig)
  
def get_expiry_status(expiry_date_str):
    """
    Determines the expiry status of a product based on its expiry date.
    Args:
    expiry_date_str: Expiry date as a string.
    Returns:
    str: HTML formatted expiry status.
    """
    try:
        expiry_date_obj = datetime.strptime(expiry_date_str, '%Y-%m-%d')
        current_date = datetime.now()

        if expiry_date_obj < current_date:
            # Red and bold for expired products
            return "<span style='color: red; font-weight: bold;'> (Expired)</span>"
        elif expiry_date_obj <= current_date + timedelta(days=7):
            # Orange and bold for products expiring soon
            return "<span style='color: orange; font-weight: bold;'> (Going to expire soon)</span>"
        else:
            return ""
    except ValueError:
        return ""  # Return empty string in case of invalid date format

def detect_device_type():
    # Get the user agent string from the query parameters
    user_agent_string = st.experimental_get_query_params().get("user_agent", [None])[0]

    if user_agent_string:
        # Check if the user agent string contains keywords for mobile or tablet devices
        if any(keyword in user_agent_string.lower() for keyword in ["mobile", "tablet", "android", "iphone", "ipad"]):
            return "Phone or Tablet"
    
    # Default to "Computer" if the user agent is not detected as mobile or tablet
    return "Computer"
