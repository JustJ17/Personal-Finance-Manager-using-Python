import json
import os
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, 'data', 'users.json')

def load_users():
    """Load users from the JSON file."""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r') as file:
        return json.load(file)
    

def save_users(users):
    """Save users to the JSON file."""
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)


def register_user():
    """Add a new user."""
    users = load_users()

    username = input("Enter your username: ").strip()
    if username in users:
        print("⚠️ Username already exists.")
        return
    
    password = input("Enter your password: ").strip()
    email = input("Enter your email: ").strip()

    users[username] = {
        'password': password,
        'email': email,
        'balance' : 0.0
    }

    save_users(users)
    print(f"✅ User '{username}' registered successfully!\n")


def login_user():
    users = load_users()

    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()



    if username in users and users[username]['password'] == password:
         print(f"✅ Welcome back, {username}!")
         return username
    else:
        print("❌ Invalid username or password.")
        return None



def get_user_balance(username):
    """Display the user’s balance."""
    users = load_users()
    if username in users:
        print(f"💰 Your current balance is: ${users[username]['balance']}")
    else:
        print("⚠️ User not found.")

def update_user_balance(username, new_balance):
    users = load_users()
    if username in users:
        users[username]['balance'] = new_balance
        save_users(users)
        print("✅ Balance updated successfully.")
    else:
        print("⚠️ User not found.")

  



