### README File Structure

1. **Project Title**: ReLife App
2. **Introduction**: Expired wasted consumables and equipment is a monumental problem in our hospital and many others around the world with both environmental and financial costs.  The unutilised waste can amount to hundreds of thousands of dollars within a hospital. Our solution is an easy to use inventory marketplace app, ReLife. 
3. **Features**: Market place app to buy and sell near-to-expiry products. Safe and secure - only users with verified email address can login
4. **Technology Stack**: Python, SQLite, Streamlit, bcrypt
5. **Component Descriptions**: Short descriptions for each component of your app.
    - `main.py`: This is the core file of the ReLife app, orchestrating the app's workflow. It initializes the database connection to users.db, setting up user, verification, and products tables. The script leverages Streamlit for the web interface, displaying a custom login form, product addition form, and admin views based on user authentication. It incorporates custom CSS for styling and supports dynamic content based on user roles, enhancing the user experience.
      
    - `database.py`: database.py serves as the foundation for the ReLife app's data management. It includes functions to interact with the SQLite database, ensuring that user and product data are structured and stored efficiently. Here's a breakdown of its components:

create_users_table(conn): Initializes the users table within the database if it does not exist. The table is designed to store user information, including first name, last name, username, email (as the primary key), password, and email verification status.

create_verification_table(conn): Sets up a verification_tokens table specifically for handling email verification processes. This table pairs user emails with their corresponding unique verification tokens.

create_products_table(conn): Constructs the products table to keep track of all product-related information. The table captures product IDs, user names (or IDs), item names, brands, types, sizes, costs, quantities, expiry dates, locations, and image paths.

add_user_name_to_users_table(conn, user_name): A utility function added to update the users table to include a new user_name column, reflecting an enhancement in the user data model.

    - `authentication.py`: Email Verification: Through integration with the SendGrid API, this component sends out verification emails to new users. It ensures that user email addresses are valid and verified, enhancing the security and reliability of user accounts.

Password Handling: Utilizes the bcrypt library to securely hash user passwords before storing them in the database. This practice safeguards user passwords against theft and unauthorized access.
User Registration and Login: Provides functions to add new users to the database with hashed passwords and to verify login credentials. It ensures that only authenticated users can access their accounts.

Verification Code Generation: Generates unique verification codes for email verification, employing uuid for code generation. This is crucial for the email verification process, ensuring a secure mechanism for confirming user emails.

Email Verification Status Update: Updates the database to reflect the verification status of a user's email, further tying into the app's security measures.

By encapsulating these functionalities, authentication.py lays the foundation for a secure user experience, ensuring that user data is handled securely and responsibly. It interacts with the database to manage user information and authentication states, playing a critical role in maintaining the integrity and security of the ReLife application.
    - `ui_components.py`: This module contains the definition and implementation of the user interface components used within the ReLife application. It leverages the Streamlit library to create a seamless and interactive user experience.
signup_form(conn): Renders the sign-up form and processes new user registrations. It integrates with the authentication module to manage user credentials and verification processes.

login_form(conn): Provides the login interface, authenticating users against stored credentials in the database. Upon successful authentication, it updates the session state to reflect the user's logged-in status.

logout(): Resets the session state, effectively logging the user out of the application.

add_product_form(conn, user_name): Displays a product submission form allowing users to add new product entries to the database, including uploading images for the products.

admin_view_by_users(conn): Exclusive to admin users, this function presents aggregated data visualizations such as cost savings by department and most frequently bought and sold items, utilizing matplotlib for charting.

display_products(conn, context=""): Lists all products from the database with search functionality. Each listing can be expanded to reveal detailed product information and images.

show_product_details_popup(product): Creates an expanded view for product details, providing a more in-depth look at individual product attributes.

load_custom_css(): Injects custom CSS to enhance the styling of the Streamlit components, ensuring the application's visual appeal aligns with the ReLife brand.

    - `utils.py`: This script encompasses a set of utility functions designed to augment the ReLife application's user interface and backend processing capabilities. It provides the following features:
local_css(file_name): Applies custom CSS to the Streamlit application for a more tailored look and feel by injecting the contents of a given CSS file.

generate_mock_transaction_data(locations, products, max_count): Simulates transaction data for demonstration purposes. This function generates random buy and sell counts for a list of products across different locations.

find_most_frequent_items(df): Aggregates transaction data to find the most frequently bought and sold items at each location. It's useful for identifying trends and popular items in inventory management.

plot_most_frequent_transactions(df): Utilizes matplotlib to create visualizations for the most frequently transacted items, helping in quick and easy interpretation of data trends.

get_expiry_status(expiry_date_str): Evaluates the expiry status of products by comparing the expiry date to the current date and returns a formatted string indicating if the product is expired or expiring soon.

detect_device_type(): Determines the type of device the Streamlit app is being viewed on, based on the user agent string. This can be useful for responsive design considerations within the app.

    - `logo.png`: The app's logo displayed in the UI.
    - `users.db`: SQLite database file containing user and product data.
    - `style.css`: Custom CSS styles for the app's UI.
    - `requirements.txt`: Lists all Python dependencies required to run the app.
6. **Installation and Setup**: Clone the repository, install the dependencies listed in `requirements.txt`. Then go to Terminal (Mac) or CMD (Windows), navigate the folder where you have cloned this repository. Type "streamlit run main.py"

### Description for main.py

For the `main.py` file, here's a concise description that can be integrated into the README under the Component Descriptions section:

- `main.py`: This is the core file of the ReLife app, orchestrating the app's workflow. It initializes the database connection to `users.db`, setting up user, verification, and products tables. The script leverages Streamlit for the web interface, displaying a custom login form, product addition form, and admin views based on user authentication. It incorporates custom CSS for styling and supports dynamic content based on user roles, enhancing the user experience.
