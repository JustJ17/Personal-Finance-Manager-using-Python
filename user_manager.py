import json
import os
import hashlib
import re

class User_Manager:
    USERS_FILE = "users.json"

    def __init__(self):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.USERS_FILE = os.path.join(self.BASE_DIR, 'data', 'users.json')
        self.users = self.load_users()

    def load_users(self):
        """Load users from the JSON file."""
        if not os.path.exists(self.USERS_FILE):
            return {}
        with open(self.USERS_FILE, 'r') as file:
            return json.load(file)

    def save_users(self):
        """Save users to the JSON file."""
        os.makedirs(os.path.dirname(self.USERS_FILE), exist_ok=True)
        with open(self.USERS_FILE, 'w') as file:
            json.dump(self.users, file, indent=4)

    def hash_password(self, password):
        """Hash a password for storing."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self):
        """Add a new user interactively."""

        # === Username Validation ===
        while True:
            username = input("Enter your username: ").strip()
            if not username:
                print("⚠️ Username cannot be empty.")
            elif len(username) < 3:
                print("⚠️ Username must be at least 3 characters long.")
            elif not username.isalnum():
                print("⚠️ Username can only contain letters and numbers.")
            elif username in self.users:
                print("⚠️ Username already exists.")
            else:
                break

        # === Password Validation ===
        while True:
            password = input(
                "Password must be at least 6 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character.\n"
                "Enter your password: "
            ).strip()
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

        hashed_pw = self.hash_password(password)

        existing_ids = [user.get("id", 0) for user in self.users.values()]
        new_id = max(existing_ids) + 1 if existing_ids else 1

        # ✅ Update the class attribute directly
        self.users[username] = {
            "id": new_id,
            "name": username,
            "password": hashed_pw,
            "email": email,
            "balance": 0.0,
            "number_of_transactions": 0,
            "monthly_budget": 0.0,
            "monthly_expenses": 0.0,
            "savings_goal": {
                "goal_name": "New Laptop",
                "target_amount": 1000
            }
        }

        # ✅ Save updated users
        self.save_users()
        print(f"✅ User '{username}' registered successfully!\nYour user ID is {new_id}.")

    def login_user(self):
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        hashed_pw = self.hash_password(password)

        if username in self.users and self.users[username]['password'] == hashed_pw:
            print(f"✅ Welcome back, {username}!")
            return self.users[username]
        else:
            print("❌ Invalid username or password.")
            return None

    def switch_user(self, current_user):
        """Switch to a different user."""
        print(f"🔄 Switching user from {current_user}")
        new_user = self.login_user()
        if new_user:
            return new_user
        return current_user

    def get_user_balance(self, username):
        """Display the user’s balance."""
        if username in self.users:
            print(f"💰 Your current balance is: ${self.users[username]['balance']}")
        else:
            print("⚠️ User not found.")

    def update_user_balance(self, username, new_balance):
        """Update the user's balance and save changes."""
        if username in self.users:
            self.users[username]['balance'] = new_balance
            self.save_users()
            print("✅ Balance updated successfully.")
        else:
            print("⚠️ User not found.")

    def set_savings_goal(self, user):
        """Set or update a savings goal."""
        goal_name = input("🎯 Enter goal name: ")
        try:
            target = float(input("💰 Enter target amount: "))
            if target <= 0:
                print("⚠️ Target must be greater than 0.")
                return
            self.users[user['name']]['savings_goal'] = {
                "goal_name": goal_name,
                "target_amount": target
            }
            self.save_users()
            print(f"✅ Savings goal '{goal_name}' set to ${target:.2f}")
        except ValueError:
            print("⚠️ Invalid amount entered.")

    def check_savings_progress(self, user):
        """Display progress toward the savings goal."""
        name = user['name']
        goal = self.users[name].get('savings_goal')
        if not goal:
            print("⚠️ No savings goal set.")
            return

        balance = self.users[name]['balance']
        target = goal['target_amount']
        percent = min((balance / target) * 100, 100)

        print(f"🎯 Goal: {goal['goal_name']} | Target: ${target:.2f}")
        print(f"💰 Current Savings: ${balance:.2f} ({percent:.1f}% achieved)")

        if percent >= 100:
            print("🏆 Congratulations! You've reached your savings goal!")

    


def banner():
    banner = r"""
    /$$      /$$           /$$                                                  
    | $$  /$ | $$          | $$                                                  
    | $$ /$$$| $$  /$$$$$$ | $$  /$$$$$$$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$       
    | $$/$$ $$ $$ /$$__  $$| $$ /$$_____/ /$$__  $$| $$_  $$_  $$ /$$__  $$      
    | $$$$_  $$$$| $$$$$$$$| $$| $$      | $$  \ $$| $$ \ $$ \ $$| $$$$$$$$      
    | $$$/ \  $$$| $$_____/| $$| $$      | $$  | $$| $$ | $$ | $$| $$_____/      
    | $$/   \  $$|  $$$$$$$| $$|  $$$$$$$|  $$$$$$/| $$ | $$ | $$|  $$$$$$$      
    |__/     \__/ \_______/|__/ \_______/ \______/ |__/ |__/ |__/ \_______/      
                                                                                
                                                                                
                                                                                
    /$$                     /$$     /$$                                       
    | $$                    |  $$   /$$/                                       
    /$$$$$$    /$$$$$$        \  $$ /$$//$$$$$$  /$$   /$$  /$$$$$$             
    |_  $$_/   /$$__  $$        \  $$$$//$$__  $$| $$  | $$ /$$__  $$            
    | $$    | $$  \ $$         \  $$/| $$  \ $$| $$  | $$| $$  \__/            
    | $$ /$$| $$  | $$          | $$ | $$  | $$| $$  | $$| $$                  
    |  $$$$/|  $$$$$$/          | $$ |  $$$$$$/|  $$$$$$/| $$                  
    \___/   \______/           |__/  \______/  \______/ |__/                  
                                                                                
                                                                                
                                                                                
    /$$$$$$$$ /$$                                                               
    | $$_____/|__/                                                               
    | $$       /$$ /$$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$              
    | $$$$$   | $$| $$__  $$ |____  $$| $$__  $$ /$$_____/ /$$__  $$             
    | $$__/   | $$| $$  \ $$  /$$$$$$$| $$  \ $$| $$      | $$$$$$$$             
    | $$      | $$| $$  | $$ /$$__  $$| $$  | $$| $$      | $$_____/             
    | $$      | $$| $$  | $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$             
    |__/      |__/|__/  |__/ \_______/|__/  |__/ \_______/ \_______/             
                                                                                
                                                                                
                                                                                
    /$$      /$$                                                                
    | $$$    /$$$                                                                
    | $$$$  /$$$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$               
    | $$ $$/$$ $$ |____  $$| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$              
    | $$  $$$| $$  /$$$$$$$| $$  \ $$| $$  \ $$| $$$$$$$$| $$  \__/              
    | $$\  $ | $$ /$$__  $$| $$  | $$| $$  | $$| $$_____/| $$                    
    | $$ \/  | $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$| $$                    
    |__/     |__/ \_______/|__/  |__/ \____  $$ \_______/|__/                    
                                    /$$  \ $$                                  
                                    |  $$$$$$/                                  
                                    \______/                                   
                                    """
    print(banner)