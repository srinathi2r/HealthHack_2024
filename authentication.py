#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:44:03 2024

@author: srinath
"""
import os
import bcrypt
import uuid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Accessing the SendGrid API key from an environment variable
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

def send_verification_email(email, verification_code):
    """
    Sends a verification email to the user with a verification code.
    Args:
    email (str): The email address to send to.
    verification_code (str): The verification code to include in the email.
    """
    message = Mail(
        from_email='srinath.svce@gmail.com',
        to_emails=email,
        subject='Verify your email',
        html_content=f'Please verify your email by entering this code: {verification_code}')

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)  # Send the email
        print("Email Sent. Response:")
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Email Send Error:", e)


def generate_verification_code():
    """
    Generates a unique verification code.
    """
    return str(uuid.uuid4())[:8]  # Example: 8-character unique code

def verify_user_email(conn, email):
    c = conn.cursor()
    c.execute('UPDATE users SET is_email_verified = ? WHERE email = ?', (True, email))
    conn.commit()
    print(f"Email Verified for user with email: {email}")

def hash_password(password):
    """
    Hashes a password using bcrypt.
    Args:
    password (str): The password to be hashed.
    Returns:
    bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def add_user(conn, first_name, last_name, email, password, user_name):
    """
    Adds a new user to the database.
    Args:
    conn: Database connection object.
    first_name (str): The first name of the user.
    last_name (str): The last name of the user.
    email (str): The email of the user.
    password (str): The password of the user.
    user_name (str): The user's full name.
    """
    # Log the inputs
    print("Sign-up Inputs - Email:", email, "Password:", password)  # Be cautious with password logging

    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('INSERT INTO users (first_name, last_name, email, password, is_email_verified, user_name) VALUES (?, ?, ?, ?, ?, ?)',
              (first_name, last_name, email, hashed_password, 0, user_name))  # Set is_email_verified to 0 for new users
    conn.commit()
    print(f"User added with email: {email}")

def verify_login(email, password, conn):
    """
    Verifies a user's login credentials and checks if the email is verified.
    Args:
    email (str): The email of the user.
    password (str): The password of the user.
    conn: Database connection object.
    Returns:
    bool: True if login is successful and email is verified, False otherwise.
    """
    # Log the inputs
    print("Login Inputs - Email:", email, "Password:", password)  # Be cautious with password logging

    c = conn.cursor()
    c.execute('SELECT password, is_email_verified FROM users WHERE email = ?', (email,))
    user_data = c.fetchone()
    if user_data is None:
        return False
    hashed_password, is_email_verified = user_data
    print(password.encode('utf-8'))
    print(hashed_password)
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password) and is_email_verified

def verify_email_code(conn, email, verification_code):
    """
    Verifies the email based on the entered verification code.
    Args:
    conn: Database connection object.
    email (str): The email of the user.
    verification_code (str): The verification code entered by the user.
    Returns:
    bool: True if the verification is successful, False otherwise.
    """
    print("Verifying email code...")
    c = conn.cursor()
    
    print(f"Received email: {email}")
    print(f"Received verification code: {verification_code}")

    # Fetch the token from the database for the given email
    c.execute('SELECT token FROM verification_tokens WHERE email = ?', (email,))
    token_data = c.fetchone()
    
    if token_data:
        fetched_token = token_data[0]
        print(f"Fetched token from the database: {fetched_token}")

    # Check if the fetched token matches the verification code
    if token_data and fetched_token == verification_code:
        # Update the is_email_verified field in the database
        c.execute('UPDATE users SET is_email_verified = ? WHERE email = ?', (True, email))
        conn.commit()
        print(f"Email Verified for user with email: {email}")
        return True
    else:
        print(f"Invalid verification code for user with email: {email}")
        return False

