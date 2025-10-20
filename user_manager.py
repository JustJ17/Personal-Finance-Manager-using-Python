import json
import os
import hashlib
import re


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
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)


def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    """Add a new user."""
    users = load_users()

      # === Username Validation ===
    while True:
        username = input("Enter your username: ").strip()
        if not username:
            print("⚠️ Username cannot be empty.")
        elif len(username) < 3:
            print("⚠️ Username must be at least 3 characters long.")
        elif not username.isalnum():
            print("⚠️ Username can only contain letters and numbers.")
        elif username in users:
            print("⚠️ Username already exists.")
        else:
            break
    
       # === Password Validation ===
    while True:
        password = input("Password must be at least 6 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character."
            "Enter your password:").strip()
        if len(password) < 6:
            print("⚠️ Password must be at least 6 characters long.")
        elif not re.search(r"[A-Z]", password):
            print("⚠️ Password must contain at least one uppercase letter.")
        elif not re.search(r"[a-z]", password):
            print("⚠️ Password must contain at least one lowercase letter.")
        elif not re.search(r"\d", password):
            print("⚠️ Password must contain at least one number.")
        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            print("⚠️ Password must contain at least one special character.")
        else:
            break
    # === Email Validation ===
    while True:
        email = input("Enter your email: ").strip()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print("⚠️ Invalid email format. Try again.")
        else:
            break
    hashed_pw = hash_password(password)

    existing_ids = [
        user.get("id", 0) for user in users.values() if isinstance(user, dict)
    ]
    last_id = max(existing_ids) if existing_ids else 0
    new_id = last_id + 1

    users[username] = {
        'id': new_id,
        'password':  hashed_pw,
        'email': email,
        'balance' : 0.0
    }

    save_users(users)
    print(f"✅ User '{username}' registered successfully!\n"
          f"   your user ID is {new_id}.")


def login_user():
    users = load_users()

    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    hashed_pw = hash_password(password)


    if username in users and users[username]['password'] == hashed_pw:
        print(f"✅ Welcome back, {username}!")
        return username
    else:
        print("❌ Invalid username or password.")
        return None


def switch_user(current_user):
    """Switch to a different user."""
    print(f"🔄 Switching user from {current_user}")
    new_user = login_user()
    if new_user:
        return new_user
    return current_user
    


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

  



