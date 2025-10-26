# 💰 Personal Finance Manager

A comprehensive console-based Python application for managing personal finances, tracking income/expenses, generating reports, and achieving financial goals.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Advanced Features](#advanced-features)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

---

## 🎯 Overview

The **Personal Finance Manager** is a Python console application that helps users:
- Track income and expenses
- Generate detailed financial reports
- Set and monitor savings goals
- Manage recurring transactions
- Filter, search, and sort transaction history
- Import/export transaction data

This project demonstrates professional programming practices including data validation, error handling, file I/O operations, and modular code architecture.

---

## ✨ Features

### Core Features

#### 👤 User Management
- **Multi-user Support**: Create and manage multiple user accounts
- **Secure Authentication**: Password hashing using SHA-256
- **User Profiles**: Store user-specific data including balance, budget, and transaction history
- **Profile Switching**: Seamlessly switch between different user accounts

#### 💳 Transaction Management
- **Add Transactions**: Record income and expenses with detailed information
- **View All Transactions**: Display comprehensive transaction history
- **Edit Transactions**: Modify existing transactions with validation
- **Delete Transactions**: Remove transactions with confirmation
- **Transaction Details**: Track amount, date, category, payment method, and description

#### 🔍 Search & Filter
- **Date Range Search**: Find transactions within specific time periods
- **Category Filter**: Filter by categories (Food, Transport, Entertainment, Other)
- **Amount Range Filter**: Search transactions by amount range
- **Sort Results**: Sort by date, amount, or category (ascending/descending)

#### 📊 Reports & Analytics
- **Dashboard Summary**: Real-time overview of income, expenses, and net balance
- **Monthly Reports**: Detailed monthly financial analysis with:
  - Total income and expenses
  - Net balance calculation
  - Most spent category
  - Category breakdown with visual bars
  - Percentage analysis
- **Category Breakdown**: All-time spending analysis by category
- **Spending Trends**: Visual chart showing monthly spending patterns across all months

#### 💾 Data Persistence
- **JSON Storage**: Secure data storage in JSON format
- **Auto-save**: Automatic saving after each operation
- **Backup System**: Automatic backup creation on startup and exit
- **Data Validation**: Input validation before saving

### 🎁 Advanced Features

#### 1️⃣ Recurring Transactions
- Set up automatic recurring income/expenses
- Configurable frequency (daily, weekly, monthly)
- Automatic processing of due transactions
- View and manage all recurring transactions

#### 2️⃣ Monthly Budget Tracker
- Set monthly spending limits
- Track current month's expenses
- Budget warnings when approaching or exceeding limit
- Month-over-month comparison

#### 3️⃣ CSV Import/Export
- Export transactions to CSV format
- Import transactions from CSV files
- Preserve all transaction details
- Easy data backup and sharing

#### 4️⃣ Savings Goals
- Set custom savings goals
- Track progress toward financial targets
- Visual progress indicators
- Goal achievement notifications

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- No external libraries required (uses Python standard library)

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/personal-finance-manager.git
cd personal-finance-manager
```

2. **Create required directories**
```bash
mkdir -p data/transactions
```

3. **Run the application**
```bash
python main.py
```

---

## 📖 Usage

### First Time Setup

1. **Register a new user**
   - Choose option `[1] Register`
   - Enter username (minimum 3 characters, alphanumeric)
   - Create a strong password (minimum 6 characters, must include uppercase, lowercase, number, and special character)
   - Provide a valid email address

2. **Login**
   - Choose option `[2] Login`
   - Enter your username and password

### Main Menu Options

```
[1]  Add Income/Expenses        - Record new transactions
[2]  View All Transactions      - Display transaction history
[3]  Edit Transactions          - Modify existing entries
[4]  Delete Transaction         - Remove a transaction
[5]  Search by Date Range       - Find transactions by date
[6]  Filter by Category         - View specific categories
[7]  Filter by Amount Range     - Search by amount
[8]  Sort Results               - Organize transaction display
[9]  Switch User                - Change active user
[10] Monthly Reports            - View monthly financial summary
[11] Category Breakdown         - All-time category analysis
[12] Spending Trends            - Visual spending chart
[13] Recurring Transactions     - Manage automatic transactions
[14] Monthly Budget Tracker     - Track budget vs spending
[15] Export to CSV              - Export transaction data
[16] Import from CSV            - Import transaction data
[0]  Exit                       - Save and quit
```

### Example Workflows

#### Adding a Transaction
1. Select `[1] Add Income/Expenses`
2. Choose transaction type (Income/Expense)
3. Enter amount (e.g., 150.75)
4. Enter date (YYYY-MM-DD) or press Enter for today
5. Select category (Food, Transport, Entertainment, Other)
6. Select payment method (Cash, Credit, Debit, Other)
7. Add description (optional)

#### Generating Monthly Report
1. Select `[10] Monthly Reports`
2. Choose month (0 for current month, or select from list)
3. View comprehensive financial summary including:
   - Total income and expenses
   - Net balance
   - Most spent category
   - Category breakdown with percentages
   - Optional: View detailed transactions

#### Setting Up Recurring Transaction
1. Select `[13] Recurring Transactions`
2. Choose `[1] Add Recurring Transaction`
3. Set up transaction details
4. Select frequency (Daily/Weekly/Monthly)
5. The system automatically processes due transactions

---

## 📁 Project Structure

```
personal-finance-manager/
│
├── main.py                              # Application entry point
├── transaction_manager.py               # Transaction operations & reports
├── user_manager.py                      # User authentication & management
├── recurring_transactions_manager.py    # Recurring transaction logic
│
├── data/
│   ├── users.json                       # User account data
│   └── transactions/
│       ├── transactions_username_id.json    # User transaction files
│       └── transactions_username_id_backup.json  # Backup files
│
└── README.md                            # This file
```

### Module Descriptions

#### `main.py`
- Application entry point
- Login/registration menu
- User session management

#### `transaction_manager.py`
- Core transaction CRUD operations
- Search, filter, and sort functionality
- Financial reports and analytics
- Data visualization (spending trends)
- CSV import/export
- Budget tracking

#### `user_manager.py`
- User registration with validation
- Secure password hashing
- User authentication
- Profile management
- Savings goal tracking

#### `recurring_transactions_manager.py`
- Recurring transaction setup
- Automatic transaction processing
- Frequency management (daily/weekly/monthly)

---

## 🛠️ Technologies Used

### Core Python Modules
- `datetime` - Date/time handling and validation
- `json` - Data persistence and serialization
- `os` - File system operations
- `shutil` - Backup file operations
- `csv` - CSV import/export functionality
- `hashlib` - Password hashing (SHA-256)
- `re` - Input validation using regex

### Data Structures
- **Dictionaries**: User profiles and transaction data
- **Lists**: Transaction collections and search results
- **Classes**: Transaction and User objects
- **Date Objects**: Proper date handling and comparison

---

## 📊 Data Format

### Transaction Structure
```json
{
    "transaction_id": "user1",
    "type": "expense",
    "user_id": 1,
    "amount": 50.00,
    "date": "2025-01-15",
    "category": "food",
    "description": "Lunch at restaurant",
    "payment_method": "credit"
}
```

### User Structure
```json
{
    "username": {
        "id": 1,
        "name": "username",
        "password": "hashed_password_sha256",
        "email": "user@example.com",
        "balance": 1500.00,
        "number_of_transactions": 25,
        "monthly_budget": 2000.00,
        "monthly_expenses": 0.0,
        "savings_goal": {
            "goal_name": "New Laptop",
            "target_amount": 1000
        }
    }
}
```

---

## 🔒 Security Features

- **Password Hashing**: All passwords are hashed using SHA-256
- **Input Validation**: Comprehensive validation for all user inputs
- **File Permissions**: Secure file handling with proper error checking
- **Data Backup**: Automatic backup creation prevents data loss
- **Session Management**: Secure user session handling

---

## 🐛 Known Issues & Limitations

1. **Single Currency**: Currently supports only one currency per user
2. **No Password Recovery**: Lost passwords cannot be recovered (by design for security)
3. **Local Storage Only**: Data stored locally, no cloud sync
4. **Console Only**: No graphical user interface

---

## 🚧 Future Enhancements

- [ ] Multi-currency support
- [ ] Budget alerts and notifications
- [ ] Graphical user interface (GUI)
- [ ] Cloud synchronization
- [ ] Mobile app version
- [ ] Advanced analytics and predictions
- [ ] Bill reminder system
- [ ] Financial health scoring
- [ ] Export to PDF reports

---

## 👥 Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Authors

- **Mohamed Gamal** 
- **Mohamed Abdelfatah** 

---

## 🙏 Acknowledgments

- Thanks to all contributors who helped improve this project
- Inspired by real-world personal finance management needs
- Built as part of Python programming course

---

## 📞 Support

For questions or issues:
- Create an issue in the GitHub repository


---

## 📸 Screenshots

### Main Menu
```
╔══════════════════════════════════════════════════════╗
║            💰 PERSONAL FINANCE MANAGER 💰            ║
╠══════════════════════════════════════════════════════╣
║ [1] Add Income / Expenses                            ║
║ [2] View All Transactions                            ║
...
╚══════════════════════════════════════════════════════╝
```

### Dashboard Summary
```
========================================
📊 DASHBOARD SUMMARY
========================================
Total Income : $5000.00
Total Expense: $2500.00
Net Balance  : $2500.00
========================================
```

---

**Made with ❤️ and Python**
