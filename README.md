🧾 Personal Finance Manager using Python
📖 Overview

The Personal Finance Manager is a command-line application built in Python that helps users track income, expenses, and manage personal finances securely.
It includes user authentication with password hashing, profile switching, balance management, and data validation for usernames, emails, and passwords.

🚀 Features

✅ User Registration & Login

Validates username, email, and password format.

Secure password hashing using hashlib.

Each user is assigned a unique auto-incrementing ID.

✅ Profile Switching

Switch between registered users without restarting the program.

Preserves session data for each user.

✅ Data Persistence

User data stored securely in a data/users.json file.

Automatically creates the directory if it doesn’t exist.

✅ Input Validation

Username: must be alphanumeric, 3+ characters.

Password: must include uppercase, lowercase, number, and special character.

Email: validated using regex pattern.

✅ Balance Tracking

Each user starts with a default balance of $0.0.

Future extension: add income, expenses, and transaction management.

🧩 Project Structure
Personal-Finance-Manager-using-Python/
│
├── data/
│   └── users.json              # Stores registered users securely
│
├── main.py                     # Main program entry point
├── user_manager.py             # Handles all user-related operations
├── README.md                   # Project documentation
└── requirements.txt (optional) # Future dependency list

🛠️ Technologies Used

Python 3

JSON for lightweight data storage

Hashlib for password encryption

Regular Expressions (re) for validation

OS module for file management

⚙️ How to Run
1️⃣ Clone the Repository
git clone https://github.com/yourusername/Personal-Finance-Manager-using-Python.git
cd Personal-Finance-Manager-using-Python

2️⃣ Run the Program
python3 main.py

3️⃣ Follow the On-Screen Menu
╔══════════════════════════════════════════════════════╗
║            💰 PERSONAL FINANCE MANAGER 💰           ║
╠══════════════════════════════════════════════════════╣
║ [1] Register                                         ║
║ [2] Login                                            ║
║ [3] Exit                                             ║
╚══════════════════════════════════════════════════════╝

🔐 Security Features

Passwords are hashed using SHA-256 before being stored.

User data is kept in a JSON file, protected by structured validation checks.

No plain-text passwords are stored.

🧠 Example Workflow
=== Welcome to the User System ===
1. Register
2. Login
3. Exit

> Choose an option: 1
Enter username: mo
Enter password: Mo@1234
Enter email: mo@gmail.com
✅ User 'mo' registered successfully!

> Choose an option: 2
Enter username: mo
Enter password: Mo@1234
✅ Welcome back, mo!
💰 Your current balance is: $0.0

🧩 Future Improvements

🚧 Planned features for next versions:

Add, edit, delete, and search transactions.

Categorize expenses and incomes.

Generate summary reports and statistics.

Export data to CSV or PDF.

Implement GUI (Tkinter or Web version).

🧑‍💻 Author

Developed by: Mo (Python Developer)
GitHub: yourusername

🪪 License

This project is open-source and available under the MIT License.