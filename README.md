### 1. Project Title
ReLife App

### 2. Introduction
Expired and wasted consumables and equipment represent a significant problem in hospitals globally, carrying both environmental and financial implications. The ReLife app is an intuitive inventory marketplace solution aimed at reducing waste and recovering value from near-expiry products.

### 3. Features
- Marketplace for buying and selling near-to-expiry products.
- Enhanced security - only verified email users can log in.

### 4. Technology Stack
- Python
- SQLite
- Streamlit
- bcrypt

### 5. Component Descriptions

#### `main.py`
The central orchestrator for the ReLife app. It establishes the database connections, sets up essential tables, and utilizes Streamlit for the user interface. It customizes the UI with CSS and dynamically adjusts the content based on user roles.

#### `database.py`
Foundation for data management in the ReLife app. It structures and maintains user and product data efficiently within the SQLite database.

- `create_users_table(conn)`
- `create_verification_table(conn)`
- `create_products_table(conn)`
- `add_user_name_to_users_table(conn, user_name)`

#### `authentication.py`
Manages user credentials, email verification, and secure password handling using bcrypt and SendGrid API for a secure user experience.

- Email Verification Process
- Password Handling
- User Registration and Login
- Verification Code Generation
- Email Verification Status Update

#### `ui_components.py`
Defines and implements the UI components for the ReLife app, ensuring a smooth user experience with Streamlit.

- `signup_form(conn)`
- `login_form(conn)`
- `logout()`
- `add_product_form(conn, user_name)`
- `admin_view_by_users(conn)`
- `display_products(conn, context="")`
- `show_product_details_popup(product)`
- `load_custom_css()`

#### `utils.py`
A collection of utility functions to enhance UI and processing capabilities.

- `local_css(file_name)`
- `generate_mock_transaction_data(locations, products, max_count)`
- `find_most_frequent_items(df)`
- `plot_most_frequent_transactions(df)`
- `get_expiry_status(expiry_date_str)`
- `detect_device_type()`

#### Additional Components
- `logo.png`: Brand logo used in the UI.
- `users.db`: SQLite database storing user and product data.
- `style.css`: Custom style definitions for the app's interface.
- `requirements.txt`: Dependencies required for the app.

### 6. Installation and Setup
Clone the repository, install the dependencies listed in `requirements.txt`. Then go to Terminal (Mac) or CMD (Windows), navigate the folder where you have cloned this repository. Type "streamlit run main.py"

