#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:47:02 2024

@author: srinath
"""
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from authentication import generate_verification_code, add_user, send_verification_email, verify_email_code, verify_login
from utils import generate_mock_transaction_data, find_most_frequent_items, plot_most_frequent_transactions, get_expiry_status

def signup_form(conn):
    """
    Displays the sign-up form and handles new user registration.
    Returns:
    str: The generated user_name.
    """
    st.subheader("Sign Up")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email Address", max_chars=50)
    user_name = f"{first_name} {last_name}"  # Generate user_name from first_name and last_name
    password = st.text_input("Password", type="password")

    verification_code_input_visible = False  # Flag to control the visibility of the verification code input
    verification_success = None  # Initialize verification success flag
    verification_code = generate_verification_code()  # Generate the verification code

    if st.button("Sign Up"):
        add_user(conn, first_name, last_name, email, password, user_name)  # Pass user_name to add_user
        send_verification_email(email, verification_code)
        verification_code_input_visible = True  # Set the flag to True

    if verification_code_input_visible:
        verification_code_input = st.text_input("Verification Code")
        if st.button("Verify Code"):
            print("Verify Code button clicked")  # Debugging statement
            if verify_email_code(conn, email, verification_code_input):  # Call the verify_email_code function
                print("Email verified successfully")  # Debugging statement
                verification_success = True
            else:
                print("Email verification failed")  # Debugging statement
                verification_success = False

    # Check verification success and provide appropriate message
    if verification_success is True:
        st.success("Email verified successfully!")
        st.markdown("You have successfully signed up. Please proceed to the login page.")
    elif verification_success is False:
        st.error("Invalid verification code. Please try again.")

    # Return the generated user_name
    return user_name


def login_form(conn):
    """
    Displays the login form and handles user authentication.
    """
    st.subheader("Login")
    email = st.text_input("Email Address", max_chars=50, key=f"login_email")
    password = st.text_input("Password", type="password", key="login_password")
    login_attempted = st.button("Login", key="login_button")
    c = conn.cursor()

    if login_attempted:
        if verify_login(email, password, conn):
            # Update session state upon successful login
            st.session_state['logged_in'] = True
            st.session_state['user_email'] = email
            # Retrieve and set the user's name for display
            c.execute('SELECT first_name, last_name FROM users WHERE email = ?', (email,))
            user_data = c.fetchone()
            if user_data:
                st.session_state['user_name'] = f"{user_data[0]} {user_data[1]}"
            # Use st.experimental_rerun to refresh the app immediately after login
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")

    # Toggle to show/hide the signup form
    if st.checkbox("New users: Click here to Sign Up"):
        signup_form(conn)

def logout():
    """
    Handles the logout process, resetting relevant session state variables.
    """
    for key in ['logged_in', 'user_email', 'user_name']:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state['just_logged_out'] = True
 

# Define the directory where uploaded images will be saved
UPLOAD_DIR = "uploads"  # You can change this to your desired directory path

def add_product_form(conn, user_name):
    """
    Displays a form for adding new products and inserts them into the database.
    Args:
    conn: Database cursor object.
    user_name (str): The name of the user adding the product.
    """
    st.header("Add a Product")
    with st.form("product_form", clear_on_submit=True):
        item_name = st.text_input("Item Name")
        brand = st.text_input("Brand")
        type_subtype = st.text_input("Type/Subtype")
        size = st.text_input("Size")
        cost = st.number_input("Cost", step=0.01)
        quantity = st.text_input("Quantity")
        expiry_date = st.date_input("Expiry Date")
        location = st.text_input("Location/Cost Centre")
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png"])

        submitted = st.form_submit_button("Submit Product")
        
        if submitted:
            try:
                # Save the uploaded image to the UPLOAD_DIR directory
                if uploaded_file is not None:
                    image_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                    with open(image_path, "wb") as image_file:
                        image_file.write(uploaded_file.read())
                else:
                    image_path = None
                
                # Insert the product details into the database
                c = conn.cursor()
                c.execute('INSERT INTO products (user_name, item_name, brand, type_subtype, size, cost, quantity, expiry_date, location, image_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (user_name, item_name, brand, type_subtype, size, cost, quantity, expiry_date, location, image_path))
                conn.commit()  # Commit the changes to the database
                st.success("Product Added")
            except Exception as e:
                st.error(f"Error adding product to database: {str(e)}")
        return submitted  # Return the submitted value

        # Check if the form has not been submitted, and don't display success message
        if not submitted:
            st.empty()  # Empty element to avoid displaying "None"

def admin_view_by_users(conn):
    """
    Displays visualizations for the admin view, including cost saved by location and mock transaction data.
    """

    # Fetch and visualize cost data by location
    c = conn.cursor()
    c.execute('SELECT location, SUM(cost) AS total_cost FROM products GROUP BY location')
    cost_data = c.fetchall()

    if cost_data:
        cost_df = pd.DataFrame(cost_data, columns=["location", "Total Cost"])
        fig, ax = plt.subplots()
        bars = ax.bar(cost_df['location'], cost_df['Total Cost'])

        # Add enhanced labels on each bar
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, yval, f"${round(yval, 2)}", 
                    va='bottom', ha='center', 
                    color='brown', fontweight='bold', fontsize=12)  # Adjust color, weight, and size as needed

        ax.set_xlabel('Location')
        ax.set_ylabel('Total Cost')
        st.subheader("Potential Cost Saved by Department")
        st.pyplot(fig)
    else:
        st.info("No location-based cost data available.")

    # Generate mock transaction data for specified locations
    locations = ["OT", "DS Ward", "SICU", "ED"]
    products = ["Lipofundin", "CPR Stat Padz", "ETT"]  # Replace with actual product names if desired
    transaction_df = generate_mock_transaction_data(locations, products)
    most_frequent_df = find_most_frequent_items(transaction_df)

    # Display mock transaction data visualization
    st.subheader("Most Frequently Bought and Sold Items by Department")
    plot_most_frequent_transactions(most_frequent_df)



def display_products(conn, context=""):
    """
    Displays a table of products from the database. Each product can be expanded to view more details in a two-column layout.
    Args:
    conn: Database cursor object.
    """
    st.header("Products List")
    search_query = st.text_input("Search by Item Name, Brand or Type/Subtype", key=f"product_search_{context}")

    c = conn.cursor()
    query = '''
    SELECT id, item_name, brand, type_subtype, size, cost, quantity, expiry_date, location, image_path 
    FROM products
   '''
    if search_query:
        query += " WHERE item_name LIKE ? OR brand LIKE ? OR type_subtype LIKE ?"
        search_query = f'%{search_query}%'
        c.execute(query, (search_query, search_query, search_query))
    else:
        c.execute(query)
    products_data = c.fetchall()

    if not products_data:
        st.warning("No products found.")
    else:
        for product in products_data:
            product_id, item_name, brand, type_subtype, size, cost, quantity, expiry_date, location, image_path = product
            with st.expander(f"{item_name}"):
                col1, col2 = st.columns([3, 2])

                # Column for Image
                with col1:
                    st.image(image_path, caption=item_name, width=300)

                # Column for Details
                with col2:
                    st.text(f"Brand: {brand}")
                    st.text(f"Type/Subtype: {type_subtype}")
                    st.text(f"Size: {size}")
                    st.text(f"Cost: {cost}")
                    st.text(f"Quantity: {quantity}")
                    st.text(f"Expiry Date: {expiry_date}")
                    st.text(f"Location: {location}")
                    expiry_status_html = get_expiry_status(expiry_date)
                    st.markdown(f"Expiry Date: {expiry_date} {expiry_status_html}", unsafe_allow_html=True)
   
                # Contact Seller Button
                st.button("Contact Seller", key=f"contact_{product_id}_{context}")


def show_product_details_popup(product):
    """
    Displays the details of the clicked product in a popup.
    Args:
    product: The product details as a Series or dict.
    """
    with st.expander("Product Details", expanded=True):
        col1, col2, col3 = st.columns([3, 3, 2])  # Adjust column ratios for better spacing

        # Column for Image
        with col1:
            st.image(product['Image Path'], caption=product['Item Name'], width=250)  # Further increase image width

        # Column for Details
        with col2:
            st.subheader(product['Item Name'])
            st.text(f"Brand: {product['Brand']}")
            st.text(f"Type/Subtype: {product['Type/Subtype']}")
            st.text(f"Size: {product['Size']}")
            st.text(f"Cost: {product['Cost']}")
            st.text(f"Quantity: {product['Quantity']}")
            st.text(f"Expiry Date: {product['Expiry Date']}")
            st.text(f"Location: {product['Location']}")

        # Column for Buttons
        with col3:
            # Custom CSS to reduce the font size of the button
            st.markdown("<style>.small-font { font-size:10px !important; }</style>", unsafe_allow_html=True)
            if st.button("Contact Seller", key=f"contact_{product['ID']}"):
                # Logic for Contact Seller button (Placeholder)
                pass
            if st.button("Close", key=f"close_{product['ID']}"):
                # Logic to close the popup
                st.experimental_rerun()
                

def load_custom_css():
    """
    Load custom CSS styles.
    """
    custom_css = """
    <style>
        /* Custom styles for buttons */
        .stButton>button {
            font-size: 10px;  /* Adjust the font size */
            padding: 4px 12px;  /* Adjust padding to make button smaller */
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
