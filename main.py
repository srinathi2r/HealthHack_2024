#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:02:50 2024

@author: srinath
"""
from database import create_users_table, create_verification_table, create_products_table
from ui_components import login_form, logout, add_product_form, admin_view_by_users, display_products, load_custom_css
from utils import local_css
import sqlite3
import streamlit as st
from PIL import Image

def main():
    local_css("style.css")
    load_custom_css()

    with sqlite3.connect('users.db') as conn:
        create_users_table(conn)
        create_verification_table(conn)
        create_products_table(conn)  # Create the products table

    # Create columns for the title, tagline, and logo
    col1, col2 = st.columns([4, 2])

    # Title and tagline in the first column with top alignment using CSS
    col1.markdown("""
        <div style='height: 100%; display: flex; flex-direction: column; justify-content: flex-start;'>
            <h1 style='font-size: 50px; margin-bottom: -15px;'>ReLife<sup style='vertical-align: super; font-size: 10px;'>TM</sup></h1>
            <h3 style='color: grey; font-style: italic; font-size: 20px; margin-top: -15px;'>Renewing Value, Reducing Waste</h3>
        </div>
        """, unsafe_allow_html=True)
    
    # Logo in the second column
    logo = Image.open('logo.png')
    col2.image(logo, width=150, use_column_width=False)

    
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login_form(conn)  # Display the login form
    else:
        user_name = st.session_state.get('user_name', 'User')
        col1, col2 = st.columns([3,1])  # Adjust the columns as per your layout
        col1.markdown(f"<h3 style='text-align: left; color: red; font-size: 20px;'>Welcome, {user_name}</h3>", unsafe_allow_html=True)
        col2.button("Logout", on_click=logout)

        if st.session_state.get('user_email') == 'srinath.svce@gmail.com':
            # Admin user tabs
            tab1, tab2, tab3 = st.tabs(["📦 View Products", "➕ Add Product", "👨‍💼 Admin View"])
            with tab1:
                display_products(conn)
            with tab2:
                add_product_form(conn, user_name)  # Removed display_products from here
            with tab3:
                admin_view_by_users(conn)
        else:
            # Regular user tabs
            tab1, tab2 = st.tabs(["📦 View Products", "➕ Add Product"])
            with tab1:
                display_products(conn)
            with tab2:
                add_product_form(conn, user_name)  # Removed display_products from here

if __name__ == "__main__":
    main()
