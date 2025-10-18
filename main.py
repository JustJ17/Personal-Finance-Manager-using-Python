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
        user = login_user()
        if user:
            get_user_balance(user)
    elif choice == "3":
        print("👋 Goodbye!")
        break
    else:
        print("❌ Invalid choice. Try again.")