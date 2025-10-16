from enum import Enum
import datetime # For date/time handling
import csv # For CSV file operations
import json # For JSON data storage
import os # For file operations
from decimal import Decimal # For accurate money calculations 
import uuid
import hashlib

class User:
    def __init__(self, name, password, currency="USD"):
        self.user_id = str(uuid.uuid4())  # auto-generate a unique user ID
        self.name = name
        self.password = self.hash_password(password)  # store only hashed version
        self.currency = currency

    def hash_password(self, password):
        """Hash the password for secure storage."""
        return hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self):
        """Convert the user object to a dictionary (for saving to JSON)."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "password": self.password,
            "currency": self.currency
        }

    def __str__(self):
        """Readable printout for debugging or display."""
        return f"User({self.name}, {self.currency})"

user1 = User("John Doe", "mysecretpassword", "USD")

# =============================================================My work starts here=================================================================

def show_menu():
    print("""
╔══════════════════════════════════════════════════════╗
║            💰 PERSONAL FINANCE MANAGER 💰            ║
╠══════════════════════════════════════════════════════╣
║ [1] Add Income / Expenses                            ║
║ [2] View All Transactions                            ║
║ [3] Edit Transactions                                ║
║ [4] Delete Transaction                               ║
║ [5] Search by Date Range                             ║
║ [6] Filter by Category                               ║
║ [7] Filter by Amount Range                           ║
║ [8] Sort Results                                     ║
║ [0] Exit                                             ║
╚══════════════════════════════════════════════════════╝
👉 Please enter your choice: """, end="")
    
def check_for_transaction_file(user):
    # Define full path to your file
    file_path = os.path.join('data', 'transactions', f'transactions_{user.name}_{user.user_id}.json')

    try:
        # Ensure the directory exists (creates folders if missing)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # If file doesn't exist, create it and write empty list
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)
            print("✅ transactions.json created successfully.")
        else:
            print("✅ transactions.json already exists.")
    
    except Exception as e:
        print(f"⚠️ Error while checking/creating file: {e}")


class Transaction:
    def __init__(self, transaction_id, type, user_id, amount, date, category, description=None, payment_method=None):

        if not isinstance(type, str) or type.lower() not in ['income', 'expense']:
            raise ValueError("Type must be 'income' or 'expense'")
        
        if not isinstance(amount, (int, float, Decimal)) or amount <= 0:
            raise ValueError("Amount must be a positive number")
        
        if not isinstance(date, datetime.date):
            raise ValueError("Date must be a datetime.date object")

        if  not isinstance(payment_method, str) or payment_method.lower() not in ['cash', 'credit', 'debit', 'other']:
            raise ValueError("Invalid payment method")

        if  not isinstance(category, str) or category.lower() not in ['food', 'transport', 'entertainment', 'other']:
            raise ValueError("Invalid category")

        self.transaction_id = transaction_id
        self.type = type
        self.user_id = user_id
        self.amount = amount
        self.date = date
        self.payment_method = payment_method
        self.description = description




while True:
    show_menu()
    choice = input().strip()

    if choice == '1':
        print("Add Income / Expenses")
        # Code to add income or expenses
    elif choice == '2':
        print("View All Transactions")
        # Code to view all transactions
    elif choice == '3':
        print("Edit Transactions")
        # Code to edit transactions
    elif choice == '4':
        print("Delete Transaction")
        # Code to delete a transaction
    elif choice == '5':
        print("Search by Date Range")
        # Code to search transactions by date range
    elif choice == '6':
        print("Filter by Category")
        # Code to filter transactions by category
    elif choice == '7':
        print("Filter by Amount Range")
        # Code to filter transactions by amount range
    elif choice == '8':
        print("Sort Results")
        # Code to sort transaction results
    elif choice == '0':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")