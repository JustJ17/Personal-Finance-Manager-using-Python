from enum import Enum
import datetime # For date/time handling
import csv # For CSV file operations
import json # For JSON data storage
import os # For file operations
from decimal import Decimal # For accurate money calculations 
import uuid
import hashlib

# =============================================================Temp User Class=================================================================
class User:
    def __init__(self, name, password, currency="USD", user_id=None):
        self.user_id = user_id or str(uuid.uuid4())  # use provided user_id or auto-generate
        self.name = name
        self.password = self.hash_password(password)  # store only hashed version
        self.currency = currency
        self.numberOfTransactions = 0

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

user1 = User("John Doe", "mysecretpassword", "USD", "user-1234")

# =============================================================Functions=================================================================

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
    
def read_transaction_file(user):
    # Define full path to your file
    file_path = os.path.join('data', 'transactions', f'transactions_{user.name}_{user.user_id}.json')

    try:
        # Ensure the directory exists (creates folders if missing)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # If file doesn't exist, create it and write empty list
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)
            # print("✅ transactions.json created successfully.")
            transactions_list = []
            return transactions_list
        else:
            # print("✅ transactions.json already exists.")
            with open(file_path, "r") as file:
                try:
                    transactions_data = json.load(file)
                    transactions_list = [Transaction.from_dict(t) for t in transactions_data]
                    user.numberOfTransactions = len(transactions_list)

                except json.JSONDecodeError:
                    print("⚠️ Warning: Transaction file was corrupted. Starting with empty transactions.") #maybe I would want to change this later
                    transactions_list = []
            return transactions_list

    except Exception as e:
        print(f"⚠️ Error while checking/creating file: {e}")

def save_transactions_to_file(user, transaction_list):
    """
    Save a list of Transaction objects to the user's JSON file.
    
    Args:
        user: User object
        transaction_list: List of Transaction objects
    """
    file_path = os.path.join('data', 'transactions', 
                             f'transactions_{user.name}_{user.user_id}.json')
    
    try:
        # Convert all Transaction objects to dictionaries
        transactions_data = [t.to_dict() for t in transaction_list]
        
        # Write to file with nice formatting
        with open(file_path, 'w') as f:
            json.dump(transactions_data, f, indent=4)
        
        print(f"✅ Successfully saved {len(transaction_list)} transactions.")
        return True
        
    except Exception as e:
        print(f"❌ Error saving transactions: {e}")
        return False

def add_transaction(user, new_transaction):
    """
    Add a new transaction to the user's file.
    
    Args:
        user: User object
        new_transaction: Transaction object to add
    """
    # Load existing transactions
    transactions = read_transaction_file(user)
    
    # Add the new one
    transactions.append(new_transaction)
    
    # Save back to file
    return save_transactions_to_file(user, transactions)

def delete_transaction(user, transaction_id):
    """
    Delete a transaction by its ID.
    
    Args:
        user: User object
        transaction_id: ID of transaction to delete
        
    Returns:
        bool: True if deleted, False if not found
    """
    # Load all transactions
    transactions = read_transaction_file(user)
    
    # Find and remove the transaction
    original_count = len(transactions)
    transactions = [t for t in transactions if t.transaction_id != transaction_id]
    
    # Check if anything was deleted
    if len(transactions) == original_count:
        print(f"❌ Transaction '{transaction_id}' not found.")
        return False
    
    # Save the updated list
    save_transactions_to_file(user, transactions)
    print(f"✅ Transaction '{transaction_id}' deleted successfully.")
    user.numberOfTransactions -= 1
    return True

def edit_transaction(user, transaction_id):
    """
    Edit an existing transaction with interactive prompts and validation.
    
    Args:
        user: User object
        transaction_id: ID of transaction to edit
        
    Returns:
        bool: True if edited successfully, False if not found
    """
    # Load all transactions
    transactions = read_transaction_file(user)
    
    # Find the transaction to edit
    target_transaction = None
    for trans in transactions:
        if trans.transaction_id == transaction_id:
            target_transaction = trans
            break
    
    # Check if transaction exists
    if not target_transaction:
        print(f"❌ Transaction '{transaction_id}' not found.")
        return False
    
    # Display current transaction details
    print("\n" + "="*60)
    print("📝 EDITING TRANSACTION")
    print("="*60)
    print(target_transaction)
    print("\n💡 Press Enter to keep current value, or enter new value\n")
    
    # ===== Edit Transaction Type =====
    print(f"Current type: {target_transaction.type}")
    print("Options: [1] Income  [2] Expense")
    type_choice = input("Enter choice (1-2) or press Enter to keep: ").strip()
    
    if type_choice:
        type_options = ["income", "expense"]
        while True:
            try:
                choice_num = int(type_choice)
                if 1 <= choice_num <= 2:
                    target_transaction.type = type_options[choice_num - 1]
                    print(f"✅ Type updated to: {target_transaction.type}")
                    break
                else:
                    print("❌ Invalid choice. Please select 1 or 2.")
                    type_choice = input("Enter choice (1-2): ").strip()
            except ValueError:
                print("❌ Please enter a number.")
                type_choice = input("Enter choice (1-2): ").strip()
    
    # ===== Edit Amount =====
    print(f"\nCurrent amount: {target_transaction.amount}")
    amount_input = input("Enter new amount or press Enter to keep: ").strip()
    
    if amount_input:
        while True:
            try:
                new_amount = float(amount_input)
                if new_amount <= 0:
                    print("❌ Amount must be positive.")
                    amount_input = input("Enter new amount: ").strip()
                    continue
                target_transaction.amount = new_amount
                print(f"✅ Amount updated to: {new_amount}")
                break
            except ValueError:
                print("❌ Please enter a valid number.")
                amount_input = input("Enter new amount: ").strip()
    
    # ===== Edit Date =====
    print(f"\nCurrent date: {target_transaction.date}")
    date_input = input("Enter new date (YYYY-MM-DD) or press Enter to keep: ").strip()
    
    if date_input:
        while True:
            try:
                new_date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
                target_transaction.date = new_date
                print(f"✅ Date updated to: {new_date}")
                break
            except ValueError:
                print("❌ Invalid date format. Use YYYY-MM-DD")
                date_input = input("Enter new date: ").strip()
                if not date_input:  # Allow user to cancel
                    break
    
    # ===== Edit Category =====
    print(f"\nCurrent category: {target_transaction.category}")
    print("Options: [1] Food  [2] Transport  [3] Entertainment  [4] Other")
    category_choice = input("Enter choice (1-4) or press Enter to keep: ").strip()
    
    if category_choice:
        category_options = ["food", "transport", "entertainment", "other"]
        while True:
            try:
                choice_num = int(category_choice)
                if 1 <= choice_num <= 4:
                    target_transaction.category = category_options[choice_num - 1]
                    print(f"✅ Category updated to: {target_transaction.category}")
                    break
                else:
                    print("❌ Invalid choice. Please select between 1 and 4.")
                    category_choice = input("Enter choice (1-4): ").strip()
            except ValueError:
                print("❌ Please enter a number.")
                category_choice = input("Enter choice (1-4): ").strip()
    
    # ===== Edit Payment Method =====
    print(f"\nCurrent payment method: {target_transaction.payment_method or 'N/A'}")
    print("Options: [1] Cash  [2] Credit  [3] Debit  [4] Other")
    payment_choice = input("Enter choice (1-4) or press Enter to keep: ").strip()
    
    if payment_choice:
        payment_options = ["cash", "credit", "debit", "other"]
        while True:
            try:
                choice_num = int(payment_choice)
                if 1 <= choice_num <= 4:
                    target_transaction.payment_method = payment_options[choice_num - 1]
                    print(f"✅ Payment method updated to: {target_transaction.payment_method}")
                    break
                else:
                    print("❌ Invalid choice. Please select between 1 and 4.")
                    payment_choice = input("Enter choice (1-4): ").strip()
            except ValueError:
                print("❌ Please enter a number.")
                payment_choice = input("Enter choice (1-4): ").strip()
    
    # ===== Edit Description =====
    print(f"\nCurrent description: {target_transaction.description or 'No description'}")
    desc_input = input("Enter new description or press Enter to keep: ").strip()
    
    if desc_input:
        target_transaction.description = desc_input
        print(f"✅ Description updated")
    
    # ===== Save Changes =====
    print("\n" + "="*60)
    confirm = input("💾 Save changes? (y/n): ").strip().lower()
    
    if confirm == 'y' or confirm == 'yes':
        if save_transactions_to_file(user, transactions):
            print("\n✅ Transaction updated successfully!")
            print("\n📋 Updated Transaction:")
            print(target_transaction)
            return True
        else:
            print("❌ Failed to save changes.")
            return False
    else:
        print("❌ Changes discarded.")
        return False

def create_transaction(current_user):

    print("\n🧾  Create a New Transaction")
    print("=" * 40)    
    t_id = current_user.name + str(current_user.numberOfTransactions)
    t_userId = current_user.user_id
    current_user.numberOfTransactions += 1
    type_options = ["income", "expense"]
    category_options = ["food", "transport", "entertainment", "other"]
    payment_options = ["cash", "credit", "debit", "other"]
    
    # ---- Transaction Type ----
    print("\nSelect transaction type:")
    for i, option in enumerate(type_options, 1):
        print(f"[{i}] {option.capitalize()}")
    while True:
        try:
            t_type_choice = int(input("Enter choice (1-2): "))
            if 1 <= t_type_choice <= len(type_options):
                t_type = type_options[t_type_choice - 1]
                break
            else:
                print("❌ Invalid choice. Please select 1 or 2.")
        except ValueError:
            print("❌ Please enter a number, not text.")

    # --- Amount input ---
    while True:
        try:
            t_amount = float(input("💰  Enter the amount (e.g., 150.75): "))
            if t_amount <= 0:
                print("❌  Amount must be positive.")
                continue
            break
        except ValueError:
            print("❌  Please enter a valid number.")

    # --- Date input ---
    while True:
        print("\n📅  Enter the transaction date:")
        print("   - Format: YYYY-MM-DD")
        print("   - Leave empty for today’s date")
        date_input = input("👉  Date: ").strip()
        if not date_input:
            t_date = datetime.datetime.today().date()
            break
        try:
            t_date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌  Invalid date format. Please try again.")  
    
    # ---- Category ----
    print("\nSelect category:")
    for i, option in enumerate(category_options, 1):
        print(f"[{i}] {option.capitalize()}")
    while True:
        try:
            t_category_choice = int(input("Enter choice (1-4): "))
            if 1 <= t_category_choice <= len(category_options):
                t_category = category_options[t_category_choice - 1]
                break
            else:
                print("❌ Invalid choice. Please select between 1 and 4.")
        except ValueError:
            print("❌ Please enter a number, not text.")

    # ---- Payment Method ----
    print("\nSelect payment method:")
    for i, option in enumerate(payment_options, 1):
        print(f"[{i}] {option.capitalize()}")
    while True:
        try:
            t_payment_choice = int(input("Enter choice (1-4): "))
            if 1 <= t_payment_choice <= len(payment_options):
                t_payment_method = payment_options[t_payment_choice - 1]
                break
            else:
                print("❌ Invalid choice. Please select between 1 and 4.")
        except ValueError:
            print("❌ Please enter a number, not text.")

    # --- Description ---
    t_description = input("\n📝  Add a short description (optional): ").strip()
    if not t_description:
        t_description = "No description provided."


    return Transaction( t_id, t_type, t_userId, t_amount, t_date, t_category, t_description, t_payment_method )

def filter_transactions_by_category(transaction_list):
    """
    Filter transactions by category.
    
    Args:
        transaction_list: List of Transaction objects
        category: Category to filter by (string)
        
    Returns:
        List of Transaction objects matching the category
    """
    category_options = ["food", "transport", "entertainment", "other"]
    print("\nSelect category You want to filter by:")
    for i, option in enumerate(category_options, 1):
        print(f"[{i}] {option.capitalize()}")
    while True:
        try:
            t_category_choice = int(input("Enter choice (1-4): "))
            if 1 <= t_category_choice <= len(category_options):
                t_category = category_options[t_category_choice - 1]
                break
            else:
                print("❌ Invalid choice. Please select between 1 and 4.")
        except ValueError:
            print("❌ Please enter a number, not text.")
    filtered = [t for t in transaction_list if t.category == t_category]
    for t in filtered:
        print(t)
    sortOrnot = input("Do you want to sort the results? (y/n): ").strip().lower()
    if sortOrnot == 'y' or sortOrnot == 'yes':
        sort_transactions(filtered)

def filter_transactions_by_amount_range(transaction_list):
    """
    Filter transactions by amount range.
    
    Args:
        transaction_list: List of Transaction objects
        min_amount: Minimum amount (float)
        max_amount: Maximum amount (float)
        
    Returns:
        List of Transaction objects within the amount range
    """
    while True:
        try:
            min_amount = float(input("Enter minimum amount: "))
            max_amount = float(input("Enter maximum amount: "))
            if min_amount < 0 or max_amount < 0:
                print("❌ Amounts must be non-negative.")
                continue
            if min_amount > max_amount:
                print("❌ Minimum cannot be greater than maximum.")
                continue
            break
        except ValueError:
            print("❌ Please enter valid numbers.")

    filtered = [t for t in transaction_list if min_amount <= t.amount <= max_amount]
    for t in filtered:
        print(t)
    sortOrnot = input("Do you want to sort the results? (y/n): ").strip().lower()
    if sortOrnot == 'y' or sortOrnot == 'yes':
        sort_transactions(filtered) 

def sort_transactions(transaction_list):
    """
    Sort transactions by a specified field.
    
    Args:
        transaction_list: List of Transaction objects
        sort_by: Field to sort by ("date", "amount", "category")
        descending: Whether to sort in descending order (bool)
    """
    valid_sort_fields = ["date", "amount", "category"]
    print("\nSelect field You want to sort by:")
    for i, option in enumerate(valid_sort_fields, 1):
        print(f"[{i}] {option.capitalize()}")
    while True:
        try:
            t_sort_choice = int(input("Enter choice (1-3): "))
            if 1 <= t_sort_choice <= len(valid_sort_fields):
                sort_by = valid_sort_fields[t_sort_choice - 1]
                break
            else:
                print("❌ Invalid choice. Please select between 1 and 3.")
        except ValueError:
            print("❌ Please enter a number, not text.")

    # Ask for sort order
    while True:
        order = input("Sort order (asc/desc): ").strip().lower()
        if order in ["asc", "desc"]:
            descending = (order == "desc")
            break
        print("❌ Invalid input. Please enter 'asc' or 'desc'.")

    # Sort the transactions
    sorted_list = sorted(transaction_list, key=lambda x: getattr(x, sort_by), reverse=descending)
    print(f"\n✅ Transactions sorted by {sort_by} in {'descending' if descending else 'ascending'} order.")
    for t in sorted_list:
        print(t)

def search_transactions_by_date_range(transaction_list):
    """
    Search transactions within a date range.
    
    Args:
        transaction_list: List of Transaction objects
        start_date: Start date (datetime.date)
        end_date: End date (datetime.date)
        
    Returns:
        List of Transaction objects within the date range
    """
    while True:
        try:
            start_input = input("Enter start date (YYYY-MM-DD): ").strip()
            end_input = input("Enter end date (YYYY-MM-DD): ").strip()
            start_date = datetime.datetime.strptime(start_input, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_input, "%Y-%m-%d").date()
            if start_date > end_date:
                print("❌ Start date cannot be after end date.")
                continue
            break
        except ValueError:
            print("❌ Invalid date format. Please try again.")

    filtered = [t for t in transaction_list if start_date <= t.date <= end_date]
    for t in filtered:
        print(t)
    
    sortOrnot = input("Do you want to sort the results? (y/n): ").strip().lower()
    if sortOrnot == 'y' or sortOrnot == 'yes':
        sort_transactions(filtered)

# =============================================================Transaction Class=================================================================


class Transaction:
    def __init__(self, transaction_id, type, user_id, amount, date, category, description=None, payment_method=None):

        self.transaction_id = transaction_id
        self.type = type
        self.user_id = user_id
        self.amount = amount
        self.category = category
        self.date = date
        self.payment_method = payment_method
        self.description = description

    def __str__(self):
        sep = "=" * 100
        # safely format optional fields
        desc = self.description if self.description else "No description"
        pm = self.payment_method if self.payment_method else "N/A"
        # ensure date prints nicely
        date_str = (
            self.date.isoformat() if hasattr(self.date, "isoformat") else str(self.date)
        )
        return (
            f"{sep}\n"
            f"{'TRANSACTION DETAILS':^72}\n"
            f"{sep}\n"
            f"Transaction ID  : {self.transaction_id}\n"
            f"Type            : {str(self.type).capitalize()}\n"
            f"User ID         : {self.user_id}\n"
            f"Amount          : {self.amount}\n"
            f"Date            : {date_str}\n"
            f"Category        : {self.category}\n"
            f"Payment Method  : {pm}\n"
            f"Description     : {desc}\n"
            f"{sep}"
        )
    
    def to_dict(self):
        """
        Convert the transaction object to a dictionary for JSON serialization.
        
        Returns:
            dict: A dictionary containing all transaction fields with the date
                  converted to ISO format string.
        """
        return {
            "transaction_id": self.transaction_id,
            "type": self.type,
            "user_id": self.user_id,
            "amount": self.amount,
            "date": self.date.isoformat() if hasattr(self.date, "isoformat") else str(self.date),
            "category": self.category,
            "description": self.description,
            "payment_method": self.payment_method
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Transaction object from a dictionary (loaded from JSON).
        
        Arguments:
            data (dict): Dictionary containing transaction data
            
        Returns:
            Transaction: A new Transaction instance
        """
        # Convert date string back to date object
        date_obj = datetime.datetime.fromisoformat(data['date']).date()
        
        return cls(
            transaction_id=data['transaction_id'],
            type=data['type'],
            user_id=data['user_id'],
            amount=data['amount'],
            date=date_obj,
            category=data['category'],
            description=data.get('description'),  # use .get() for optional fields
            payment_method=data.get('payment_method')
        )

# =============================================================Main Menu=================================================================

current_user = user1
def Transaction_Manager():
    while True:   
        show_menu()
        choice = input().strip()
        transaction_list = read_transaction_file(current_user)  # Ensure file exists before operations
        if choice == '1':
            # Code to add income/expense
            new_transaction = create_transaction(current_user)
            add_transaction(current_user, new_transaction)

        elif choice == '2':
            # Code to view all transactions
            for t in transaction_list:
                print(t)

        elif choice == '3':
            # Code to edit a transaction
            transaction_id = input("Enter Transaction ID to edit: ").strip()
            edit_transaction(current_user, transaction_id)
            
        elif choice == '4':
            # Code to delete a transaction
            transaction_id = input("Enter Transaction ID to delete: ").strip()
            delete_transaction(current_user, transaction_id)

        elif choice == '5':
            search_transactions_by_date_range(transaction_list)
            # Code to search transactions by date range

        elif choice == '6':
            filter_transactions_by_category(transaction_list)
            # Code to filter transactions by category

        elif choice == '7':
            filter_transactions_by_amount_range(transaction_list)
            # Code to filter transactions by amount range
            
        elif choice == '8':
            sort_transactions(transaction_list)
            # Code to sort transaction results

        elif choice == '0':
            print("Exiting the program. Goodbye!")
            return
        else:
            print("Invalid choice. Please try again.")