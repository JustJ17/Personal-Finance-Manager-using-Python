import datetime # For date/time handling
import json # For JSON data storage
import os
import shutil # For file operations
from recurring_transactions_manager import *
import csv


# =============================================================Functions=================================================================

def show_menu():
    print("""
╔══════════════════════════════════════════════════════╗
║            💰 PERSONAL FINANCE MANAGER 💰           ║
╠══════════════════════════════════════════════════════╣
║ [1] Add Income / Expenses                            ║
║ [2] View All Transactions                            ║
║ [3] Edit Transactions                                ║
║ [4] Delete Transaction                               ║
║ [5] Search by Date Range                             ║
║ [6] Filter by Category                               ║
║ [7] Filter by Amount Range                           ║
║ [8] Sort Results                                     ║
║ [9] Monthly Budget Tracker                           ║
║ [10] Monthly Reports                                 ║
║ [11] Category Breakdown                              ║
║ [12] Spending Trends                                 ║
║ [13] Recurring Transactions                          ║
║ [14] Export Transactions to CSV                      ║
║ [15] Import Transactions from CSV                    ║
║ [0] Exit                                             ║
╚══════════════════════════════════════════════════════╝
👉 Please enter your choice: """, end="")
    
def read_transaction_file(user):
    # Define full path to your file
    file_path = os.path.join('data', 'transactions', f'transactions_{user["name"]}_{user["id"]}.json')

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
                    user["number_of_transactions"] = len(transactions_list)

                except json.JSONDecodeError:
                    print("⚠️ Warning: Transaction file was corrupted. Starting with empty transactions.") #maybe I would want to change this later
                    transactions_list = []
            return transactions_list

    except Exception as e:
        print(f"⚠️ Error while checking/creating file: {e}")
        return []

def save_transactions_to_file(user, transaction_list):
    """
    Save a list of Transaction objects to the user's JSON file.
    
    Args:
        user: User object
        transaction_list: List of Transaction objects
    """
    file_path = os.path.join('data', 'transactions', 
                             f'transactions_{user["name"]}_{user["id"]}.json')
    
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

def export_transactions_to_csv(user):
    """Export all transactions of the user to a CSV file."""
    transactions = read_transaction_file(user)
    if not transactions:
        print("⚠️ No transactions to export.")
        return

    filename = f"{user['name']}_transactions.csv"
    fieldnames = ["transaction_id", "type", "user_id", "amount", "date", "category", "description", "payment_method"]
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows([t.to_dict() for t in transactions])
    
    print(f"✅ Transactions exported successfully to '{filename}'.")

def import_transactions_from_csv(user):
    """Import transactions from a CSV file into the user's record."""
    filename = f"{user['name']}_transactions.csv"
    
    if not os.path.exists(filename):
        print(f"⚠️ No CSV file found for user {user['name']}.")
        return

    with open(filename, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        transactions_data = list(reader)
    
    if not transactions_data:
        print("⚠️ The CSV file is empty.")
        return
    
    # Convert CSV data to Transaction objects
    transactions = []
    for t in transactions_data:
        # Convert string values to proper types
        if "amount" in t:
            t["amount"] = float(t["amount"])
        if "user_id" in t:
            t["user_id"] = int(t["user_id"]) if t["user_id"].isdigit() else t["user_id"]
        
        # Note: from_dict() will handle date conversion internally
        # Create Transaction object from dict
        transaction = Transaction.from_dict(t) # I change to dict because I know that my save function expects dicts, and it will be easier this way rather than implementing a save in this function
        transactions.append(transaction)
    
    save_transactions_to_file(user, transactions)
    print(f"✅ Transactions imported successfully from '{filename}'.")

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
    user["number_of_transactions"] -= 1
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
    t_id = current_user["name"] + str(current_user["number_of_transactions"] + 1)
    t_userId = current_user["id"]
    current_user["number_of_transactions"] += 1
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

def dashboard_summary(transaction_list):
    """
    Display a summary dashboard of transactions.
    
    Args:
        transaction_list: List of Transaction objects
    """
    if not transaction_list:
        print("\n" + "="*40)
        print("📊 DASHBOARD SUMMARY")
        print("="*40)
        print("No transactions found.")
        print("="*40 + "\n")
        return
    
    total_income = sum(t.amount for t in transaction_list if t.type == "income")
    total_expense = sum(t.amount for t in transaction_list if t.type == "expense")
    net_balance = total_income - total_expense

    print("\n" + "="*40)
    print("📊 DASHBOARD SUMMARY")
    print("="*40)
    print(f"Total Income : ${total_income:.2f}")
    print(f"Total Expense: ${total_expense:.2f}")
    print(f"Net Balance  : ${net_balance:.2f}")
    print("="*40 + "\n")

def monthly_report(transaction_list):
        """
        Generate a monthly financial report with income, expenses, net balance, and most spent category.
        
        Args:
            transaction_list: List of Transaction objects
        """
        if not transaction_list:
            print("❌ No transactions found. Cannot generate report.")
            return
        
        # Step 1: Get all unique months from transactions
        available_months = {}  # {(year, month): "display_string"}
        current_date = datetime.datetime.now()
        current_month = (current_date.year, current_date.month)
        
        for trans in transaction_list:
            year = trans.date.year
            month = trans.date.month
            month_key = (year, month)
            
            if month_key not in available_months:
                month_name = datetime.datetime(year, month, 1).strftime("%B %Y")
                available_months[month_key] = month_name
        
        # Sort months chronologically (oldest to newest)
        sorted_months = sorted(available_months.keys())
        
        if not sorted_months:
            print("❌ No valid dates found in transactions.")
            return
        
        # Step 2: Display menu with current month option
        print("\n" + "="*60)
        print("📅 MONTHLY REPORT - SELECT MONTH")
        print("="*60)
        
        # Check if current month has transactions
        if current_month in available_months:
            print("[0] Current Month (Default) - " + available_months[current_month])
            print("-" * 60)
        
        print("Available months:")
        for i, month_key in enumerate(sorted_months, 1):
            marker = " ← Current" if month_key == current_month else ""
            print(f"[{i}] {available_months[month_key]}{marker}")
        
        print("="*60)
        
        # Step 3: Get user choice
        while True:
            choice_input = input("👉 Select month (0 for current, or number): ").strip()
            
            # Default to current month if empty and current month exists
            if not choice_input:
                if current_month in available_months:
                    selected_month = current_month
                    break
                else:
                    print("❌ Current month has no transactions. Please select a valid month.")
                    continue
            
            try:
                choice = int(choice_input)
                
                # Option 0: Current month
                if choice == 0:
                    if current_month in available_months:
                        selected_month = current_month
                        break
                    else:
                        print("❌ No transactions in current month. Please select another.")
                        continue
                
                # Option 1-N: Specific month
                elif 1 <= choice <= len(sorted_months):
                    selected_month = sorted_months[choice - 1]
                    break
                else:
                    print(f"❌ Invalid choice. Please select between 0 and {len(sorted_months)}.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Step 4: Filter transactions for selected month
        selected_year, selected_month_num = selected_month
        monthly_transactions = [
            t for t in transaction_list 
            if t.date.year == selected_year and t.date.month == selected_month_num
        ]
        
        if not monthly_transactions:
            print(f"❌ No transactions found for {available_months[selected_month]}.")
            return
        
        # Step 5: Calculate statistics
        total_income = sum(t.amount for t in monthly_transactions if t.type == "income")
        total_expense = sum(t.amount for t in monthly_transactions if t.type == "expense")
        net_balance = total_income - total_expense
        
        # Step 6: Find most spent category
        category_spending = {}
        for trans in monthly_transactions:
            if trans.type == "expense":
                if trans.category not in category_spending:
                    category_spending[trans.category] = 0
                category_spending[trans.category] += trans.amount
        
        most_spent_category = None
        max_spent = 0
        if category_spending:
            most_spent_category = max(category_spending, key=category_spending.get)
            max_spent = category_spending[most_spent_category]
        
        # Step 7: Display the report
        month_display = available_months[selected_month]
        
        print("\n" + "="*70)
        print(f"📊 MONTHLY REPORT - {month_display.upper()}")
        print("="*70)
        print(f"📅 Period: {month_display}")
        print(f"📝 Total Transactions: {len(monthly_transactions)}")
        print("-"*70)
        
        print(f"\n💰 INCOME")
        print(f"   Total Income:     ${total_income:>12,.2f}")
        
        print(f"\n💸 EXPENSES")
        print(f"   Total Expenses:   ${total_expense:>12,.2f}")
        
        print(f"\n📈 NET BALANCE")
        balance_symbol = "+" if net_balance >= 0 else ""
        balance_indicator = "✅" if net_balance >= 0 else "⚠️"
        print(f"   {balance_indicator} Net Balance:     {balance_symbol}${net_balance:>12,.2f}")
        
        if most_spent_category:
            print(f"\n🏆 MOST SPENT CATEGORY")
            print(f"   Category: {most_spent_category.capitalize()}")
            print(f"   Amount:   ${max_spent:>12,.2f}")
            if total_expense > 0:
                percentage = (max_spent / total_expense) * 100
                print(f"   Percentage of total expenses: {percentage:.1f}%")
        else:
            print(f"\n🏆 MOST SPENT CATEGORY")
            print(f"   No expenses recorded this month")
        
        # Step 8: Category breakdown (optional, but useful)
        if category_spending:
            print(f"\n📊 EXPENSE BREAKDOWN BY CATEGORY")
            print("-"*70)
            # Sort categories by spending (highest first)
            sorted_categories = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)
            for category, amount in sorted_categories:
                percentage = (amount / total_expense) * 100 if total_expense > 0 else 0
                bar_length = int(percentage / 5)  # 20 chars max (100% / 5)
                bar = "█" * bar_length
                print(f"   {category.capitalize():<15} ${amount:>10,.2f}  {percentage:>5.1f}% {bar}")
        
        print("="*70 + "\n")
        
        # Step 9: Ask if user wants to see detailed transactions
        show_details = input("Would you like to see detailed transactions? (y/n): ").strip().lower()
        if show_details == 'y' or show_details == 'yes':
            print("\n" + "="*70)
            print(f"📋 DETAILED TRANSACTIONS - {month_display.upper()}")
            print("="*70)
            
            # Group by type
            income_trans = [t for t in monthly_transactions if t.type == "income"]
            expense_trans = [t for t in monthly_transactions if t.type == "expense"]
            
            if income_trans:
                print("\n💰 INCOME TRANSACTIONS:")
                print("-"*70)
                for trans in sorted(income_trans, key=lambda x: x.date):
                    print(f"   {trans.date} | ${trans.amount:>10,.2f} | {trans.category:<15} | {trans.description}")
            
            if expense_trans:
                print("\n💸 EXPENSE TRANSACTIONS:")
                print("-"*70)
                for trans in sorted(expense_trans, key=lambda x: x.date):
                    print(f"   {trans.date} | ${trans.amount:>10,.2f} | {trans.category:<15} | {trans.description}")
            
            print("="*70 + "\n")        

def category_breakdown(transaction_list):
    """
    Display a breakdown of all transactions by category (all time).
    Shows total income and expense breakdown by category.
    
    Args:
        transaction_list: List of Transaction objects
    """
    if not transaction_list:
        print("❌ No transactions found. Cannot generate breakdown.")
        return
    
    # Step 1: Calculate total income (all categories combined)
    total_income = sum(t.amount for t in transaction_list if t.type == "income")
    
    # Step 2: Sum expenses by category
    expense_by_category = {}
    for trans in transaction_list:
        if trans.type == "expense":
            if trans.category not in expense_by_category:
                expense_by_category[trans.category] = 0
            expense_by_category[trans.category] += trans.amount
    
    # Step 3: Calculate totals
    total_expense = sum(expense_by_category.values())
    net_balance = total_income - total_expense
    
    # Step 4: Display the report
    print("\n" + "="*70)
    print("📊 CATEGORY BREAKDOWN - ALL TIME")
    print("="*70)
    
    # Income section
    print(f"\n💰 INCOME (All Categories)")
    print(f"   Total Income:     ${total_income:>12,.2f}")
    
    # Expense section
    print(f"\n💸 EXPENSES BY CATEGORY")
    print("-"*70)
    
    if expense_by_category:
        # Sort categories by amount (highest to lowest)
        sorted_categories = sorted(expense_by_category.items(), 
                                   key=lambda x: x[1], 
                                   reverse=True)
        
        for category, amount in sorted_categories:
            percentage = (amount / total_expense) * 100 if total_expense > 0 else 0
            bar_length = int(percentage / 5)  # Visual bar (max 20 chars)
            bar = "█" * bar_length
            print(f"   {category.capitalize():<15} ${amount:>10,.2f}  {percentage:>5.1f}% {bar}")
        
        print("-"*70)
        print(f"   {'TOTAL EXPENSES':<15} ${total_expense:>10,.2f}")
    else:
        print("   No expenses recorded.")
    
    # Net balance
    print(f"\n📈 SUMMARY")
    print("-"*70)
    balance_symbol = "+" if net_balance >= 0 else ""
    balance_indicator = "✅" if net_balance >= 0 else "⚠️"
    print(f"   Total Income:     ${total_income:>12,.2f}")
    print(f"   Total Expenses:   ${total_expense:>12,.2f}")
    print(f"   {balance_indicator} Net Balance:     {balance_symbol}${net_balance:>12,.2f}")
    
    print("="*70 + "\n")

def show_monthly_budget(user):
    """
    Show this month's total expenses and compare them to a set budget.
    """
    transactions = read_transaction_file(user)
    if not transactions:
        print("❌ No transactions found.")
        return

    # Get current month and filter only expenses
    current_month = datetime.datetime.now().strftime("%Y-%m")
    monthly_expenses = [
        t.amount for t in transactions
        if t.type == "expense" and t.date.strftime("%Y-%m") == current_month
    ]
    
    total_spent = sum(monthly_expenses)
    
    # Default budget limit
    monthly_limit = user["monthly_budget_limit"]     
    print("\n" + "="*50)
    print("📅 MONTHLY BUDGET TRACKER")
    print("="*50)
    print(f"Month: {current_month}")
    print(f"Total Spent: ${total_spent:.2f}")
    print(f"Budget Limit: ${monthly_limit:.2f}")
    remaining = monthly_limit - total_spent
    if remaining >= 0:
        print(f"✅ You have ${remaining:.2f} remaining this month.")
    else:
        print(f"⚠️ You are over budget by ${abs(remaining):.2f}!")
    print("="*50 + "\n")

    new_budget = input("Would you like to set a new budget limit? (y/n): ")
    if new_budget.lower() == "y":
        while True:
            try:
                monthly_limit = float(input("Enter new budget limit: $"))
                user["monthly_budget_limit"]     = monthly_limit
                print(f"✅ New budget limit set: ${monthly_limit:.2f}")
                break
            except ValueError:
                print("❌ Invalid input. Please enter a valid number.")

def spending_trends(transaction_list):
    """
    Display spending trends across all months with visual representation.
    Shows which months had the highest spending.
    
    Args:
        transaction_list: List of Transaction objects
    """
    if not transaction_list:
        print("❌ No transactions found. Cannot generate trends.")
        return
    
    # Step 1: Group expenses by month
    monthly_spending = {}  # {(year, month): total_spending}
    
    for trans in transaction_list:
        if trans.type == "expense":
            year = trans.date.year
            month = trans.date.month
            month_key = (year, month)
            
            if month_key not in monthly_spending:
                monthly_spending[month_key] = 0
            monthly_spending[month_key] += trans.amount
    
    if not monthly_spending:
        print("❌ No expense transactions found.")
        return
    
    # Step 2: Sort months chronologically
    sorted_months = sorted(monthly_spending.keys())
    
    # Step 3: Find the maximum spending for scaling
    max_spending = max(monthly_spending.values())
    
    # Step 4: Calculate average spending
    avg_spending = sum(monthly_spending.values()) / len(monthly_spending)
    
    # Step 5: Display the trend report
    print("\n" + "="*80)
    print("📈 SPENDING TRENDS - ALL TIME")
    print("="*80)
    print(f"Months tracked: {len(sorted_months)}")
    print(f"Average monthly spending: ${avg_spending:,.2f}")
    print(f"Highest monthly spending: ${max_spending:,.2f}")
    print("="*80)
    
    # Step 6: Display visual chart
    print("\n📊 MONTHLY SPENDING CHART")
    print("-"*80)
    
    for month_key in sorted_months:
        year, month = month_key
        amount = monthly_spending[month_key]
        
        # Format month name
        month_name = datetime.datetime(year, month, 1).strftime("%b %Y")
        
        # Calculate bar length (scale to 50 characters max)
        bar_length = int((amount / max_spending) * 50) if max_spending > 0 else 0
        bar = "█" * bar_length
        
        # Indicator if above/below average
        indicator = "🔥" if amount > avg_spending else "  "
        
        # Display the bar chart
        print(f"{month_name:<12} {indicator} ${amount:>10,.2f} {bar}")
    
    print("-"*80)
    print("🔥 = Above average spending")
    print("="*80)
    
    # Step 7: Find highest and lowest spending months
    highest_month = max(monthly_spending, key=monthly_spending.get)
    lowest_month = min(monthly_spending, key=monthly_spending.get)
    
    highest_name = datetime.datetime(highest_month[0], highest_month[1], 1).strftime("%B %Y")
    lowest_name = datetime.datetime(lowest_month[0], lowest_month[1], 1).strftime("%B %Y")
    
    print(f"\n🏆 HIGHEST SPENDING MONTH")
    print(f"   {highest_name}: ${monthly_spending[highest_month]:,.2f}")
    
    print(f"\n💚 LOWEST SPENDING MONTH")
    print(f"   {lowest_name}: ${monthly_spending[lowest_month]:,.2f}")
    
    # Step 8: Calculate trend (spending increasing or decreasing?)
    if len(sorted_months) >= 2:
        first_month_spending = monthly_spending[sorted_months[0]]
        last_month_spending = monthly_spending[sorted_months[-1]]
        
        difference = last_month_spending - first_month_spending
        percentage_change = (difference / first_month_spending * 100) if first_month_spending > 0 else 0
        
        print(f"\n📉 TREND ANALYSIS")
        if difference > 0:
            print(f"   ⬆️ Spending has INCREASED by ${difference:,.2f} ({percentage_change:+.1f}%)")
            print(f"   From ${first_month_spending:,.2f} ({sorted_months[0][0]}-{sorted_months[0][1]:02d}) to ${last_month_spending:,.2f} ({sorted_months[-1][0]}-{sorted_months[-1][1]:02d})")
        elif difference < 0:
            print(f"   ⬇️ Spending has DECREASED by ${abs(difference):,.2f} ({percentage_change:.1f}%)")
            print(f"   From ${first_month_spending:,.2f} ({sorted_months[0][0]}-{sorted_months[0][1]:02d}) to ${last_month_spending:,.2f} ({sorted_months[-1][0]}-{sorted_months[-1][1]:02d})")
        else:
            print(f"   ➡️ Spending has remained STABLE")
    
    print("="*80 + "\n")

def create_backup_transaction_file(user):
    """
    Create a backup of the user's transaction file.
    
    Args:
        user: User object
    """
    original_file = os.path.join('data', 'transactions', f'transactions_{user["name"]}_{user["id"]}.json')
    backup_file = os.path.join('data', 'transactions', f'transactions_{user["name"]}_{user["id"]}_backup.json')

    try:
        if os.path.exists(original_file):
            shutil.copyfile(original_file, backup_file)
            print(f"✅ Backup created: {backup_file}")
        else:
            print(f"⚠️ No transaction file found to backup.")
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
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

def Transaction_Manager(current_user):
    """
    Main transaction management loop for the user.
    """
    create_backup_transaction_file(current_user)
    while True:
        transaction_list = read_transaction_file(current_user)  # Ensure file exists before operations
        dashboard_summary(transaction_list)
        check_recurring_transactions(current_user)
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
        
        elif choice == '9':
            show_monthly_budget(current_user)
            # Code to track monthly budget
        
        elif choice == '10':
            monthly_report(transaction_list)
            # Code to generate monthly reports

        elif choice == '11':
            category_breakdown(transaction_list)
            # Code to generate category breakdown
        
        elif choice == '12':
            spending_trends(transaction_list)
            # Code to analyze spending trends

        elif choice == '13':
            recurring_transactions_menu(current_user)
            # Code to add recuring transactions
        
        elif choice == "14":
            export_transactions_to_csv(current_user)
            # Code to export transactions to CSV

        elif choice == "15":
            import_transactions_from_csv(current_user)
            # Code to import transactions from CSV
            
        elif choice == '0':
            print("Returning to main menu!")
            create_backup_transaction_file(current_user)
            return
        else:
            print("Invalid choice. Please try again.")