from user_manager import *
from transaction_manager import *

print("=== Welcome to the User System ===")
while True:
    
   
    print("""
        ╔══════════════════════════════════════════════════════╗
        ║            💰 PERSONAL FINANCE MANAGER 💰            ║
        ╠══════════════════════════════════════════════════════╣
        ║ [1] Register                                         ║
        ║ [2] Login                                            ║
        ║ [3] Exit                                             ║
        ╚══════════════════════════════════════════════════════╝
        👉 Please enter your choice: """)
  
    choice = input("Choose an option: ").strip()

    if choice == "1":
        register_user()
    elif choice == "2":
        current_user = login_user()
        if current_user:
            Transaction_Manager(current_user)
            if  choice == "9":
                if current_user:
                 current_user = switch_user(current_user)
                 get_user_balance(current_user)
            elif choice == "2":
                continue
            else:
             print("⚠️ No user currently logged in. Please log in first.")

    elif choice == "3":
        print("👋 Goodbye!")
        break
    else:
        print("❌ Invalid choice. Try again.")