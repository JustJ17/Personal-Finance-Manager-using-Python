from user_manager import *
from transaction_manager import *
from recurring_transactions_manager import *

user_manager = User_Manager()

banner()

while True:
    
   
    print("""
        ╔══════════════════════════════════════════════════════╗
        ║            💰 PERSONAL FINANCE MANAGER 💰           ║
        ╠══════════════════════════════════════════════════════╣
        ║ [1] Register                                         ║
        ║ [2] Login                                            ║
        ║ [3] Exit                                             ║
        ╚══════════════════════════════════════════════════════╝
        👉 Please enter your choice: """)
  
    choice = input("Choose an option: ").strip()

    if choice == "1":
        user_manager.register_user()
    elif choice == "2":
        current_user = user_manager.login_user()
        if current_user:
            Transaction_Manager(current_user)
    elif choice == "3":
        print("👋 Goodbye!")
        break
    else:
        print("❌ Invalid choice. Try again.")