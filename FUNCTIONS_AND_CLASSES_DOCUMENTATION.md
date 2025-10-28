# Functions and Classes Documentation

This document provides a comprehensive overview of all functions and classes in the Personal Finance Manager application, including their purposes, steps, and relationships.

---

## Table of Contents

1. [Transaction Manager Module](#transaction-manager-module)
   - [Classes](#transaction-manager-classes)
   - [Functions](#transaction-manager-functions)
2. [Recurring Transactions Manager Module](#recurring-transactions-manager-module)
   - [Classes](#recurring-transactions-manager-classes)
   - [Functions](#recurring-transactions-manager-functions)

---

## Transaction Manager Module

### Transaction Manager Classes

#### `Transaction`

**Purpose:** Represents a single financial transaction (income or expense) with all associated details.

**Attributes:**
- `transaction_id` (str): Unique identifier for the transaction
- `type` (str): Type of transaction ("income" or "expense")
- `user_id` (int): ID of the user who owns this transaction
- `amount` (float): Monetary value of the transaction
- `date` (datetime.date): Date when the transaction occurred
- `category` (str): Category of the transaction (food, transport, entertainment, other)
- `description` (str, optional): Additional notes about the transaction
- `payment_method` (str, optional): Method of payment (cash, credit, debit, other)

**Relationships:** 
- This class is used by the `RecurringTransaction` class as a composition relationship (RecurringTransaction contains a Transaction instance)
- No inheritance relationships

**Methods:**

##### `__init__(transaction_id, type, user_id, amount, date, category, description=None, payment_method=None)`
Initializes a new Transaction object with the provided parameters.

##### `__str__()`
Returns a formatted string representation of the transaction for display purposes.

**Steps:**
1. Creates a separator line for visual formatting
2. Safely handles optional fields (description and payment_method)
3. Converts date to ISO format string
4. Returns a nicely formatted multi-line string with all transaction details

##### `to_dict()`
Converts the Transaction object to a dictionary suitable for JSON serialization.

**Steps:**
1. Creates a dictionary with all transaction attributes
2. Converts the date to ISO format string for JSON compatibility
3. Returns the dictionary

##### `from_dict(data)` (Class Method)
Creates a Transaction object from a dictionary (typically loaded from JSON).

**Steps:**
1. Extracts all fields from the input dictionary
2. Converts the date string back to a datetime.date object
3. Returns a new Transaction instance with the extracted data

---

### Transaction Manager Functions

#### `show_menu()`

**Purpose:** Displays the main menu interface for the Personal Finance Manager application.

**Steps:**
1. Prints a formatted menu with all available options (15 features + exit)
2. Uses box-drawing characters for visual appeal
3. Prompts user for input without a newline

**Parameters:** None

**Returns:** None

---

#### `read_transaction_file(user)`

**Purpose:** Reads and loads all transactions for a specific user from their JSON file.

**Steps:**
1. Constructs the file path using the user's name and ID
2. Creates the directory structure if it doesn't exist
3. If the file doesn't exist, creates it with an empty list
4. If the file exists, reads the JSON data
5. Converts each dictionary to a Transaction object
6. Updates the user's transaction count
7. Handles corrupted files by returning an empty list with a warning
8. Returns the list of Transaction objects

**Parameters:**
- `user` (dict): User dictionary containing name and id

**Returns:** List of Transaction objects

---

#### `save_transactions_to_file(user, transaction_list)`

**Purpose:** Saves a list of Transaction objects to the user's JSON file.

**Steps:**
1. Constructs the file path using user's name and ID
2. Converts all Transaction objects to dictionaries using `to_dict()`
3. Writes the data to the JSON file with proper formatting (indent=4)
4. Prints success message with transaction count
5. Returns True on success, False on error

**Parameters:**
- `user` (dict): User dictionary
- `transaction_list` (list): List of Transaction objects to save

**Returns:** bool (True if successful, False otherwise)

---

#### `add_transaction(user, new_transaction)`

**Purpose:** Adds a new transaction to the user's transaction file.

**Steps:**
1. Loads existing transactions using `read_transaction_file()`
2. Appends the new transaction to the list
3. Saves the updated list back to the file
4. Returns the result of the save operation

**Parameters:**
- `user` (dict): User dictionary
- `new_transaction` (Transaction): Transaction object to add

**Returns:** bool (success status from save operation)

---

#### `export_transactions_to_csv(user)`

**Purpose:** Exports all user transactions to a CSV file for external use or backup.

**Steps:**
1. Loads all transactions using `read_transaction_file()`
2. Checks if there are transactions to export
3. Creates a filename based on the user's name
4. Defines CSV field names matching transaction attributes
5. Opens CSV file in write mode
6. Writes header row with field names
7. Converts each Transaction to dictionary and writes as CSV rows
8. Prints success message with filename

**Parameters:**
- `user` (dict): User dictionary

**Returns:** None

---

#### `import_transactions_from_csv(user)`

**Purpose:** Imports transactions from a CSV file into the user's transaction record.

**Steps:**
1. Constructs filename based on user's name
2. Checks if the CSV file exists
3. Opens and reads the CSV file using DictReader
4. Converts CSV data to a list of dictionaries
5. Checks if the file is empty
6. Iterates through each row and converts string values to proper types:
   - Converts amount to float
   - Converts user_id to int
7. Creates Transaction objects from dictionaries using `from_dict()`
8. Saves all transactions using `save_transactions_to_file()`
9. Prints success message

**Parameters:**
- `user` (dict): User dictionary

**Returns:** None

---

#### `delete_transaction(user, transaction_id)`

**Purpose:** Deletes a specific transaction by its ID.

**Steps:**
1. Loads all transactions using `read_transaction_file()`
2. Stores the original count of transactions
3. Filters out the transaction with the matching ID using list comprehension
4. Compares the new count with the original count
5. If no change, prints error message and returns False
6. If deleted, saves the updated list
7. Decrements the user's transaction count
8. Prints success message and returns True

**Parameters:**
- `user` (dict): User dictionary
- `transaction_id` (str): ID of the transaction to delete

**Returns:** bool (True if deleted, False if not found)

---

#### `edit_transaction(user, transaction_id)`

**Purpose:** Provides an interactive interface to edit an existing transaction with validation.

**Steps:**
1. Loads all transactions
2. Searches for the transaction with the matching ID
3. If not found, prints error and returns False
4. Displays current transaction details
5. For each editable field (type, amount, date, category, payment_method, description):
   - Shows current value
   - Prompts for new value (or Enter to keep current)
   - Validates input in a loop until valid
   - Updates the field if new value provided
6. After all fields, asks for confirmation
7. If confirmed, saves the updated transactions
8. Returns True on success, False if cancelled or error

**Parameters:**
- `user` (dict): User dictionary
- `transaction_id` (str): ID of the transaction to edit

**Returns:** bool (True if edited successfully, False otherwise)

---

#### `create_transaction(current_user)`

**Purpose:** Interactive function to create a new transaction with user input and validation.

**Steps:**
1. Generates a unique transaction ID using username and transaction count
2. Increments the user's transaction count
3. Prompts for transaction type with menu:
   - Validates input is 1 or 2
   - Maps to "income" or "expense"
4. Prompts for amount:
   - Validates input is a positive number
   - Converts to float
5. Prompts for date:
   - Accepts YYYY-MM-DD format
   - Allows empty input for today's date
   - Validates date format
6. Prompts for category with menu (food, transport, entertainment, other):
   - Validates input is 1-4
   - Maps to category string
7. Prompts for payment method with menu (cash, credit, debit, other):
   - Validates input is 1-4
   - Maps to payment method string
8. Prompts for optional description
9. Creates and returns a new Transaction object

**Parameters:**
- `current_user` (dict): Current user dictionary

**Returns:** Transaction object

---

#### `filter_transactions_by_category(transaction_list)`

**Purpose:** Filters and displays transactions matching a selected category.

**Steps:**
1. Displays category menu (food, transport, entertainment, other)
2. Prompts user to select a category
3. Validates input is 1-4
4. Maps selection to category string
5. Filters transactions using list comprehension
6. Prints all matching transactions
7. Asks if user wants to sort results
8. If yes, calls `sort_transactions()` with filtered list

**Parameters:**
- `transaction_list` (list): List of Transaction objects to filter

**Returns:** None

---

#### `filter_transactions_by_amount_range(transaction_list)`

**Purpose:** Filters and displays transactions within a specified amount range.

**Steps:**
1. Prompts for minimum amount
2. Validates min_amount is a non-negative number
3. Prompts for maximum amount
4. Validates max_amount is greater than or equal to min_amount
5. Filters transactions where amount is between min and max (inclusive)
6. Prints all matching transactions
7. Asks if user wants to sort results
8. If yes, calls `sort_transactions()` with filtered list

**Parameters:**
- `transaction_list` (list): List of Transaction objects to filter

**Returns:** None

---

#### `sort_transactions(transaction_list)`

**Purpose:** Sorts and displays transactions by a user-selected field and order.

**Steps:**
1. Displays sort field menu (date, amount, category)
2. Prompts user to select a field
3. Validates input is 1-3
4. Maps selection to field name
5. Prompts for sort order (asc/desc)
6. Validates order input
7. Maps to boolean (True for descending, False for ascending)
8. Sorts transaction list using lambda function with `getattr()`
9. Prints all sorted transactions

**Parameters:**
- `transaction_list` (list): List of Transaction objects to sort

**Returns:** None

---

#### `search_transactions_by_date_range(transaction_list)`

**Purpose:** Searches and displays transactions within a specified date range.

**Steps:**
1. Prompts for start date (YYYY-MM-DD format)
2. Validates and converts to datetime.date object
3. Prompts for end date (YYYY-MM-DD format)
4. Validates and converts to datetime.date object
5. Validates end_date is not before start_date
6. Filters transactions where date is between start and end (inclusive)
7. Prints all matching transactions
8. Asks if user wants to sort results
9. If yes, calls `sort_transactions()` with filtered list

**Parameters:**
- `transaction_list` (list): List of Transaction objects to search

**Returns:** None

---

#### `dashboard_summary(transaction_list)`

**Purpose:** Displays a summary dashboard showing total income, expenses, and net balance.

**Steps:**
1. Checks if transaction list is empty
2. If empty, displays message and returns
3. Calculates total income by summing all transactions with type "income"
4. Calculates total expense by summing all transactions with type "expense"
5. Calculates net balance (income - expense)
6. Displays formatted summary with:
   - Total Income
   - Total Expense
   - Net Balance
7. All amounts formatted with $ and 2 decimal places

**Parameters:**
- `transaction_list` (list): List of Transaction objects

**Returns:** None

---

#### `monthly_report(transaction_list)`

**Purpose:** Generates a comprehensive monthly financial report with statistics and category breakdown.

**Steps:**
1. Validates transaction list is not empty
2. Extracts all unique months from transactions
3. Gets current month for default selection
4. Displays menu of available months with current month highlighted
5. Prompts user to select a month (0 for current, or number from list)
6. Validates selection
7. Filters transactions for the selected month
8. Calculates statistics:
   - Total income
   - Total expense
   - Net balance
   - Category spending breakdown
9. Identifies most spent category
10. Displays comprehensive report with:
    - Period information
    - Transaction count
    - Income section
    - Expense section
    - Net balance with indicator (✅ or ⚠️)
    - Most spent category with percentage of total
    - Category breakdown sorted by spending
11. Asks if user wants to see detailed transactions
12. If yes, displays all transactions grouped by type (income/expense)

**Parameters:**
- `transaction_list` (list): List of Transaction objects

**Returns:** None

---

#### `category_breakdown(transaction_list)`

**Purpose:** Displays a comprehensive breakdown of all transactions by category across all time.

**Steps:**
1. Validates transaction list is not empty
2. Calculates total income (all income transactions combined)
3. Groups expenses by category using a dictionary
4. Calculates total expense by summing all category values
5. Calculates net balance (income - expense)
6. Displays report with sections:
   - Total income (all categories)
   - Expenses by category (sorted highest to lowest)
   - Percentage of total expenses for each category
   - Total expenses sum
   - Summary with income, expenses, and net balance
7. Uses visual indicators (✅ or ⚠️) for positive/negative balance

**Parameters:**
- `transaction_list` (list): List of Transaction objects

**Returns:** None

---

#### `show_monthly_budget(user)`

**Purpose:** Shows current month's expenses compared to budget limit and allows updating the limit.

**Steps:**
1. Loads all user transactions
2. Checks if transactions exist
3. Gets current month in YYYY-MM format
4. Filters only expense transactions from current month
5. Calculates total spent amount
6. Retrieves user's monthly budget limit
7. Displays report with:
   - Current month
   - Total spent
   - Budget limit
   - Remaining budget or overspend amount
8. Shows ✅ if under budget, ⚠️ if over budget
9. Asks if user wants to set a new budget limit
10. If yes, prompts for new limit with validation

**Parameters:**
- `user` (dict): User dictionary

**Returns:** None

---

#### `spending_trends(transaction_list)`

**Purpose:** Displays spending trends across all months with visual bar chart representation.

**Steps:**
1. Validates transaction list is not empty
2. Groups all expense transactions by month (year, month tuple)
3. Checks if any expenses exist
4. Sorts months chronologically
5. Finds maximum spending for chart scaling
6. Calculates average monthly spending
7. Displays header with statistics:
   - Number of months tracked
   - Average monthly spending
   - Highest monthly spending
8. For each month:
   - Formats month name (e.g., "Jan 2024")
   - Calculates bar length proportional to spending (max 50 characters)
   - Adds 🔥 indicator if above average
   - Displays bar chart with amount
9. Identifies and displays:
   - Highest spending month
   - Lowest spending month
10. Calculates trend analysis:
    - Compares first and last month
    - Shows increase/decrease percentage
    - Indicates if spending is rising or falling

**Parameters:**
- `transaction_list` (list): List of Transaction objects

**Returns:** None

---

#### `create_backup_transaction_file(user)`

**Purpose:** Creates a backup copy of the user's transaction file.

**Steps:**
1. Constructs original file path
2. Constructs backup file path (adds "_backup" suffix)
3. Checks if original file exists
4. If exists, copies original to backup using `shutil.copy2()`
5. Prints success message
6. If original doesn't exist, prints warning
7. Handles any exceptions and prints error message

**Parameters:**
- `user` (dict): User dictionary

**Returns:** None

---

#### `Transaction_Manager(current_user)`

**Purpose:** Main transaction management loop that serves as the entry point for all transaction operations.

**Steps:**
1. Creates a backup of transactions at start
2. Enters infinite loop:
   - Loads current transaction list
   - Displays dashboard summary
   - Checks for due recurring transactions
   - Shows main menu
   - Gets user choice
   - Reloads transaction list (ensures fresh data)
   - Routes to appropriate function based on choice:
     - [1] Add Income/Expense
     - [2] View All Transactions
     - [3] Edit Transaction
     - [4] Delete Transaction
     - [5] Search by Date Range
     - [6] Filter by Category
     - [7] Filter by Amount Range
     - [8] Sort Results
     - [9] Monthly Budget Tracker
     - [10] Monthly Reports
     - [11] Category Breakdown
     - [12] Spending Trends
     - [13] Recurring Transactions
     - [14] Export to CSV
     - [15] Import from CSV
     - [0] Exit
   - Handles invalid choices with error message
3. Exits when user chooses [0]

**Parameters:**
- `current_user` (dict): Current logged-in user dictionary

**Returns:** None

---

## Recurring Transactions Manager Module

### Recurring Transactions Manager Classes

#### `RecurringTransaction`

**Purpose:** Represents a transaction that repeats on a schedule (weekly or monthly), wrapping a Transaction object with frequency and scheduling information.

**Attributes:**
- `transaction` (Transaction): An instance of the Transaction class
- `frequency` (str): Recurrence pattern ("monthly" or "weekly")
- `next_date` (datetime.date): The next scheduled date for this transaction

**Relationships:**
- **Composition with Transaction class**: RecurringTransaction contains a Transaction instance as an attribute
- No inheritance relationships
- Depends on Transaction class methods (`to_dict()`, `from_dict()`)

**Methods:**

##### `__init__(transaction, frequency, next_date)`
Initializes a new RecurringTransaction object.

**Steps:**
1. Stores the Transaction object
2. Stores the frequency string
3. Stores the next occurrence date

##### `__str__()`
Returns a formatted string representation of the recurring transaction.

**Steps:**
1. Creates separator line
2. Prints header
3. Embeds the transaction's string representation
4. Adds frequency and next date information
5. Returns complete formatted string

##### `to_dict()`
Converts the RecurringTransaction to a dictionary for JSON serialization.

**Steps:**
1. Calls `to_dict()` on the embedded Transaction object
2. Adds frequency field
3. Converts next_date to ISO format string
4. Returns the complete dictionary

##### `from_dict(data)` (Class Method)
Creates a RecurringTransaction object from a dictionary.

**Steps:**
1. Imports Transaction class (to avoid circular import)
2. Creates Transaction object from the nested transaction dictionary
3. Extracts frequency
4. Converts next_date string to datetime.date object
5. Returns new RecurringTransaction instance

---

### Recurring Transactions Manager Functions

#### `recurring_transactions_menu(current_user)`

**Purpose:** Displays and handles the recurring transactions submenu.

**Steps:**
1. Enters infinite loop
2. Displays menu with options:
   - [1] Add Recurring Transaction
   - [2] View Recurring Transactions
   - [3] Delete Recurring Transaction
   - [0] Return to Transaction Manager
3. Gets user choice
4. Routes to appropriate function based on choice
5. Breaks loop if user chooses [0]
6. Displays error for invalid choices

**Parameters:**
- `current_user` (dict): Current user dictionary

**Returns:** None

---

#### `read_recurring_transaction_file(user)`

**Purpose:** Reads and loads all recurring transactions for a specific user from their JSON file.

**Steps:**
1. Constructs file path in 'RecurringTransactions' directory
2. Creates directory structure if it doesn't exist
3. If file doesn't exist:
   - Creates file with empty list
   - Returns empty list
4. If file exists:
   - Reads JSON data
   - Converts each dictionary to RecurringTransaction object using `from_dict()`
   - Updates user's transaction count
   - Handles JSON decode errors by returning empty list
5. Returns list of RecurringTransaction objects
6. Handles exceptions and returns empty list on error

**Parameters:**
- `user` (dict): User dictionary

**Returns:** List of RecurringTransaction objects

---

#### `save_recurring_transactions_to_file(user, transaction_list)`

**Purpose:** Saves a list of RecurringTransaction objects to the user's JSON file.

**Steps:**
1. Constructs file path
2. Converts all RecurringTransaction objects to dictionaries using `to_dict()`
3. Writes to JSON file with formatting (indent=4)
4. Prints success message with count
5. Returns True on success
6. Catches exceptions, prints error, returns False

**Parameters:**
- `user` (dict): User dictionary
- `transaction_list` (list): List of RecurringTransaction objects

**Returns:** bool (True if successful, False otherwise)

---

#### `add_recurring_transaction(current_user)`

**Purpose:** Interactive function to create and add a new recurring transaction.

**Steps:**
1. Displays header
2. Imports `create_transaction` function (to avoid circular import)
3. Calls `create_transaction()` to get base Transaction object
4. If transaction creation failed, returns early
5. Prompts for frequency:
   - [1] Monthly
   - [2] Weekly
   - Validates input
6. Prompts for next occurrence date (YYYY-MM-DD format):
   - Validates date format
   - Converts to datetime.date object
7. Creates RecurringTransaction object
8. Loads existing recurring transactions
9. Appends new recurring transaction
10. Saves to file
11. Prints success message

**Parameters:**
- `current_user` (dict): Current user dictionary

**Returns:** None

---

#### `view_recurring_transactions(current_user)`

**Purpose:** Displays all recurring transactions for the current user.

**Steps:**
1. Displays header
2. Loads recurring transactions using `read_recurring_transaction_file()`
3. Checks if list is empty
4. If empty, prints message and returns
5. If not empty:
   - Enumerates through transactions starting at 1
   - Prints transaction number
   - Prints full transaction details using `__str__()`

**Parameters:**
- `current_user` (dict): Current user dictionary

**Returns:** None

---

#### `delete_recurring_transaction(current_user)`

**Purpose:** Allows user to delete a recurring transaction by selecting from a list.

**Steps:**
1. Displays header
2. Loads recurring transactions
3. Checks if list is empty
4. If empty, prints message and returns
5. Displays all recurring transactions with numbers
6. Prompts user to enter number of transaction to delete
7. Validates input is an integer
8. Validates selection is within valid range (1 to list length)
9. If valid:
   - Removes transaction from list using `pop()`
   - Saves updated list
   - Prints success message
10. If invalid, prints error message
11. Handles ValueError for non-numeric input

**Parameters:**
- `current_user` (dict): Current user dictionary

**Returns:** None

---

#### `check_recurring_transactions(current_user)`

**Purpose:** Checks for recurring transactions that are due today or overdue and prompts user to apply them.

**Steps:**
1. Gets today's date
2. Loads all recurring transactions
3. Filters for transactions where next_date is today or earlier
4. If due transactions found:
   - Displays "Bills Reminder" header
   - Prints all due transactions
   - Asks if user wants to apply them now (Y/N)
   - If yes, calls `apply_recurring_transactions()`
   - Prints success message
5. If no due transactions:
   - Prints "No bills due Today" message

**Parameters:**
- `current_user` (dict): Current user dictionary

**Returns:** None

---

#### `apply_recurring_transactions(current_user)`

**Purpose:** Applies all due recurring transactions and updates their next occurrence dates.

**Steps:**
1. Imports `add_transaction` (to avoid circular import)
2. Gets today's date
3. Loads all recurring transactions
4. Initializes update flag to False
5. Iterates through each recurring transaction:
   - Checks if next_date is today or earlier
   - If due:
     - Adds the transaction using `add_transaction()`
     - Prints confirmation
     - Updates next_date based on frequency:
       - For monthly: Increments month (handles year rollover)
       - For weekly: Adds 7 days
     - Uses while loop to handle multiple missed occurrences
     - Prints new next_date
     - Sets update flag to True
6. If any updates were made:
   - Saves updated recurring transactions to file

**Parameters:**
- `current_user` (dict): Current user dictionary

**Returns:** None

---

## Class Relationships Summary

### Inheritance
- **None**: No classes in this system use inheritance

### Composition
- **RecurringTransaction → Transaction**: RecurringTransaction contains a Transaction object as an attribute
  - The RecurringTransaction class wraps a Transaction object to add scheduling functionality
  - RecurringTransaction delegates transaction data to its embedded Transaction instance

### Dependencies
- **RecurringTransaction depends on Transaction**: 
  - Uses Transaction's `to_dict()` and `from_dict()` methods for serialization
  - Requires Transaction class to be imported in `from_dict()` method
- **Recurring transaction functions depend on transaction functions**:
  - `add_recurring_transaction()` imports and uses `create_transaction()`
  - `apply_recurring_transactions()` imports and uses `add_transaction()`

### Module Interaction
- Both modules work together through circular imports handled by late importing
- Transaction Manager is the main module that imports recurring_transactions_manager
- Recurring transaction functions import specific functions from transaction_manager as needed
- User data flows between both modules through dictionary objects

---

## Key Design Patterns

1. **Data Access Layer**: Functions like `read_transaction_file()` and `save_transactions_to_file()` provide abstraction for file operations

2. **Factory Pattern**: `from_dict()` class methods act as factory methods to create objects from dictionaries

3. **Serialization Pattern**: `to_dict()` methods enable easy conversion to JSON-compatible format

4. **Menu-Driven Architecture**: Both modules use menu functions that route user input to appropriate handlers

5. **Validation Loop Pattern**: Most input functions use while loops with try-except blocks for robust validation

6. **Lazy Import**: Circular dependency resolution through function-level imports rather than module-level imports

---

*Document generated on: October 28, 2025*
