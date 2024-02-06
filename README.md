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

    - `authentication.py`: 
Email Verification: Through integration with the SendGrid API, this component sends out verification emails to new users. It ensures that user email addresses are valid and verified, enhancing the security and reliability of user accounts.

Password Handling: Utilizes the bcrypt library to securely hash user passwords before storing them in the database. This practice safeguards user passwords against theft and unauthorized access.
User Registration and Login: Provides functions to add new users to the database with hashed passwords and to verify login credentials. It ensures that only authenticated users can access their accounts.

Verification Code Generation: Generates unique verification codes for email verification, employing uuid for code generation. This is crucial for the email verification process, ensuring a secure mechanism for confirming user emails.

Email Verification Status Update: Updates the database to reflect the verification status of a user's email, further tying into the app's security measures.

By encapsulating these functionalities, authentication.py lays the foundation for a secure user experience, ensuring that user data is handled securely and responsibly. It interacts with the database to manage user information and authentication states, playing a critical role in maintaining the integrity and security of the ReLife application.
    - `ui_components.py`: Defines the user interface components, such as forms and view functions.
    - `utils.py`: Includes utility functions, like CSS loader for styling.
    - `logo.png`: The app's logo displayed in the UI.
    - `users.db`: SQLite database file containing user and product data.
    - `style.css`: Custom CSS styles for the app's UI.
    - `requirements.txt`: Lists all Python dependencies required to run the app.
6. **Installation and Setup**: Instructions on how to set up and run your app locally. This should include steps like cloning the repository, installing dependencies listed in `requirements.txt`, and commands to run the app.
7. **Usage**: A brief guide on how to use the app, possibly with screenshots or GIFs for clarity.
8. **Contributing**: Guidelines for how others can contribute to the project.
9. **License**: Information about the project's license.

### Description for main.py

For the `main.py` file, here's a concise description that can be integrated into the README under the Component Descriptions section:

- `main.py`: This is the core file of the ReLife app, orchestrating the app's workflow. It initializes the database connection to `users.db`, setting up user, verification, and products tables. The script leverages Streamlit for the web interface, displaying a custom login form, product addition form, and admin views based on user authentication. It incorporates custom CSS for styling and supports dynamic content based on user roles, enhancing the user experience.

### README Length

A README file on GitHub can be as long or as short as necessary to convey the project's details effectively. The key is to balance comprehensiveness with brevity, ensuring that readers can quickly understand what your project does, how to set it up, and how to use it. Including the descriptions provided, structured appropriately within the README file, will help achieve this balance without making it unnecessarily long.
