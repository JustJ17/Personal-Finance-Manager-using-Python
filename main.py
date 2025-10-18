from user_manager import *

print("=== Welcome to the User System ===")
while True:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        register_user()
    elif choice == "2":
        current_user = login_user()
        if current_user:
            get_user_balance(current_user)
            print("Choose 1 to Switch User")
            print("2. back to Main Menu")
            choice = input("Choose an option: ").strip()
            if  choice == "3":
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