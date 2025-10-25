<<<<<<< HEAD
from user_manager import User_Manager

user_manager = User_Manager()
=======
from user_manager import *
from transaction_manager import *
>>>>>>> Gimy

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
        user_manager.register_user()
    elif choice == "2":
        current_user = user_manager.login_user()
        if current_user:
<<<<<<< HEAD
            user_manager.get_user_balance(current_user)
            print( ''' 
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
                        ║ [9] Switch User                                      ║
                        ║ [0] back to Main Menu                                ║
                        ╚══════════════════════════════════════════════════════╝
               ''')
            choice = input("Choose an option: ").strip()
=======
            Transaction_Manager(current_user)
>>>>>>> Gimy
            if  choice == "9":
                if current_user:
                    current_user = user_manager.switch_user(current_user)
                    user_manager.get_user_balance(current_user)
            elif choice == "2":
                continue
            else:
             print("⚠️ No user currently logged in. Please log in first.")

    elif choice == "3":
        print("👋 Goodbye!")
        break
    else:
        print("❌ Invalid choice. Try again.")