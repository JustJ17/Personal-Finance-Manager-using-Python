from enum import Enum
import datetime # For date/time handling
import json # For JSON data storage
import os # For file operations

class RecurringTransaction:
    def __init__(self, transaction, frequency, next_date):
        self.transaction = transaction  # Instance of Transaction
        self.frequency = frequency      # e.g., 'monthly', 'weekly'
        self.next_date = next_date      # datetime.date object

    def __str__(self):
        sep = "=" * 100
        return (
            f"{sep}\n"
            f"{'RECURRING TRANSACTION DETAILS':^72}\n"
            f"{sep}\n"
            f"{self.transaction}\n"
            f"Frequency       : {self.frequency}\n"
            f"Next Occurrence: {self.next_date}\n"
            f"{sep}"
        )
    
    def to_dict(self):
        """
        Convert the recurring transaction object to a dictionary for JSON serialization.
        
        Returns:
            dict: A dictionary containing all transaction fields with the date
                  converted to ISO format string.
        """
        return {
            "transaction": self.transaction.to_dict(),
            "frequency": self.frequency,
            "next_date": self.next_date.isoformat() if hasattr(self.next_date, "isoformat") else str(self.next_date)
        }

    @classmethod
    def from_dict(cls, data):
        """
        Create a RecurringTransaction object from a dictionary (loaded from JSON).

        Arguments:
            data (dict): Dictionary containing recurring transaction data

        Returns:
            RecurringTransaction: A new RecurringTransaction instance
        """
        transaction = Transaction.from_dict(data['transaction'])
        frequency = data['frequency']
        next_date = datetime.datetime.fromisoformat(data['next_date']).date()

        return cls(
            transaction=transaction,
            frequency=frequency,
            next_date=next_date
        )
        
    
def recurring_transactions_menu(current_user):
    """Display the recurring transactions menu and handle user choices."""
    while True:
        print("\n" + "="*40)
        print("🔁 RECURRING TRANSACTIONS MENU")
        print("="*40)
        print("[1] Add Recurring Transaction")
        print("[2] View Recurring Transactions")
        print("[3] Delete Recurring Transaction")
        print("[0] Return to Transaction Manager")
        print("="*40)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            add_recurring_transaction(current_user)
        elif choice == '2':
            view_recurring_transactions(current_user)
        elif choice == '3':
            delete_recurring_transaction(current_user)
        elif choice == '0':
            print("Returning to Transaction Manager...")
            break
        else:
            print("❌ Invalid choice. Please try again.")

def read_recurring_transaction_file(user):
    # Define full path to your file
    file_path = os.path.join('data', 'RecurringTransactions', f'RecurringTransactions_{user.name}_{user.user_id}.json')

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
                    transactions_list = [RecurringTransaction.from_dict(t) for t in transactions_data]
                    user.numberOfTransactions = len(transactions_list)

                except json.JSONDecodeError:
                    print("⚠️ Warning: Transaction file was corrupted. Starting with empty transactions.") #maybe I would want to change this later
                    transactions_list = []
            return transactions_list

    except Exception as e:
        print(f"⚠️ Error while checking/creating file: {e}")

def save_recurring_transactions_to_file(user, transaction_list):
    """
    Save a list of RecurringTransaction objects to the user's JSON file.

    Args:
        user: User object
        transaction_list: List of RecurringTransaction objects
    """
    file_path = os.path.join('data', 'RecurringTransactions', 
                             f'RecurringTransactions_{user.name}_{user.user_id}.json')

    try:
        # Convert all RecurringTransaction objects to dictionaries
        transactions_data = [t.to_dict() for t in transaction_list]
        
        # Write to file with nice formatting
        with open(file_path, 'w') as f:
            json.dump(transactions_data, f, indent=4)
        
        print(f"✅ Successfully saved {len(transaction_list)} transactions.")
        return True
        
    except Exception as e:
        print(f"❌ Error saving transactions: {e}")
        return False
    
def add_recurring_transaction(current_user):
    print("\n" + "="*40)
    print("➕ ADD RECURRING TRANSACTION")
    print("="*40)
    
    transaction = create_transaction(current_user)
    if transaction is None:
        print("❌ Transaction creation failed. Returning to menu.")
        return
    while True:
        frequency = input("Select frequency 1 (monthly) or 2 (weekly): ").strip().lower()
        if frequency not in ['1', '2']:
            print("❌ Invalid frequency. Please enter '1' for monthly or '2' for weekly.")
            continue
        next_date_str = input("Enter next occurrence date (YYYY-MM-DD): ").strip()
        try:
            next_date = datetime.datetime.strptime(next_date_str, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            continue
    recurring_transaction = RecurringTransaction(transaction, frequency, next_date)
    transactions = read_recurring_transaction_file(current_user)
    transactions.append(recurring_transaction)
    if save_recurring_transactions_to_file(current_user, transactions):
        print("✅ Recurring transaction added successfully.")

def view_recurring_transactions(current_user):
    print("\n" + "="*40)
    print("👀 VIEW RECURRING TRANSACTIONS")
    print("="*40)
    
    transactions = read_recurring_transaction_file(current_user)
    if not transactions:
        print("No recurring transactions found.")
        return
    
    for i, rt in enumerate(transactions, start=1):
        print(f"\nRecurring Transaction #{i}")
        print(rt)

def delete_recurring_transaction(current_user):
    print("\n" + "="*40)
    print("🗑️ DELETE RECURRING TRANSACTION")
    print("="*40)
    
    transactions = read_recurring_transaction_file(current_user)
    if not transactions:
        print("No recurring transactions to delete.")
        return
    
    for i, rt in enumerate(transactions, start=1):
        print(f"\nRecurring Transaction #{i}")
        print(rt)
    
    try:
        choice = int(input(f"Enter the number of the transaction to delete (1-{len(transactions)}): ").strip())
        if 1 <= choice <= len(transactions):
            deleted_transaction = transactions.pop(choice - 1)
            if save_recurring_transactions_to_file(current_user, transactions):
                print("✅ Recurring transaction deleted successfully.")
        else:
            print("❌ Invalid choice. No transaction deleted.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")

def check_recurring_transactions(current_user):
    """
    Check for due recurring transactions for the current user.
    
    Args:
        current_user: User object
    """
    today = datetime.date.today()
    transactions = read_recurring_transaction_file(current_user)
    due_transactions = [rt for rt in transactions if rt.next_date <= today]

    if due_transactions:
        print("\n" + "="*40)
        print("🔔 Bills Reminder!")
        print("="*40)
        for rt in due_transactions:
            print(rt)
        print("="*40 + "\n")
        print("Do You Want To Apply Them Now? (Y/N)")
        choice = input().strip().lower()
        if choice == 'y':
            apply_recurring_transactions(current_user)
            print("✅ Bills applied successfully.")
    else:
        print("No bills due Today.")

def apply_recurring_transactions(current_user):
    """
    Check and apply due recurring transactions for the current user.
    
    Args:
        current_user: User object
    """
    today = datetime.date.today()
    transactions = read_recurring_transaction_file(current_user)
    updated = False

    for rt in transactions:
        if rt.next_date <= today:
            # Apply the transaction
            current_user.add_transaction(rt.transaction)
            print(f"✅ Applied a recurring transaction:\n{rt.transaction}")

            # Update next occurrence date based on frequency
            if rt.frequency == 'monthly':
                month = rt.next_date.month + 1 if rt.next_date.month < 12 else 1
                year = rt.next_date.year + 1 if month == 1 else rt.next_date.year
                rt.next_date = rt.next_date.replace(year=year, month=month)
            elif rt.frequency == 'weekly':
                rt.next_date += datetime.timedelta(weeks=1)
            # Add more frequency handling as needed

            updated = True

    if updated:
        save_recurring_transactions_to_file(current_user, transactions)