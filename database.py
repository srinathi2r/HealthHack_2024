#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 11:40:22 2024

@author: srinath
"""

import streamlit as st
import sqlite3

def create_users_table(conn):
    """
    Creates a 'users' table in the SQLite database if it doesn't already exist.
    """
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
                    first_name TEXT,
                    last_name TEXT,
                    user_name TEXT,
                    email TEXT PRIMARY KEY,
                    password TEXT,
                    is_email_verified BOOLEAN DEFAULT FALSE)''')


def create_verification_table(conn):
    """
    Creates a table for storing email verification tokens.
    """
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS verification_tokens(email TEXT PRIMARY KEY, token TEXT)')


def create_products_table(conn):
    """
    Creates a 'products' table in the SQLite database if it doesn't already exist.
    """
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_name TEXT,  -- Add a column for user_name (or user_id)
                    item_name TEXT,
                    brand TEXT,
                    type_subtype TEXT,
                    size TEXT,
                    cost REAL,
                    quantity TEXT,
                    expiry_date DATE,
                    location TEXT,
                    image_path TEXT)''')

def add_user_name_to_users_table(conn, user_name):
    """
    Adds the 'user_name' field to the 'users' table.
    Args:
    conn: Database connection object.
    user_name (str): The user's name.
    """
    c = conn.cursor()
    c.execute('ALTER TABLE users ADD COLUMN user_name TEXT')
    c.execute('UPDATE users SET user_name = ? WHERE email = ?', (user_name, st.session_state['user_email']))
    conn.commit()