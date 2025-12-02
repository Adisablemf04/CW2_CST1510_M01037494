import bcrypt
import os

USER_DATA_FILE = "user.txt"

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_str = bcrypt.hashpw(password_bytes, salt)
    return hashed_str

def verify_password(plain_text_password, hashed_password):
    password_bytes = plain_text_password.encode('utf-8')
    if isinstance(hashed_password, str):
        hashed_bytes = hashed_password.encode('utf-8')
    else:
        hashed_bytes = hashed_password
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def register_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        open(USER_DATA_FILE, 'w').close()

    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            if line.strip():
                stored_username, _ = line.strip().split(',', 1)
                if stored_username == username:
                    print("Username already exists.")
                    return False

    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password.decode('utf-8')}\n")

    print("User registered successfully.")
    return True

def user_exists(username):
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            if line.strip():
                stored_username, _ = line.strip().split(',', 1)
                if stored_username == username:
                    return True
    return False

def login_user(username, password):
    # Step 1: Handle case where no users are registered yet
    if not os.path.exists(USER_DATA_FILE):
        print("No users registered yet.")
        return False

    # Step 2: Search for the username in the file
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            if line.strip():
                stored_username, stored_hash = line.strip().split(',', 1)
                if stored_username == username:
                    # Step 3: Verify the password
                    if verify_password(password, stored_hash):
                        print("Login successful.")
                        return True
                    else:
                        print("Incorrect password.")
                        return False

    # Step 4: Username not found
    print("Username not found.")
    return False

def validate_username(username):
    if not username:
        return False, "Username cannot be empty."
    if len(username) < 4:
        return False, "Username must be at least 4 characters long."
    if not username.isalnum():
        return False, "Username must contain only letters and numbers."
    return True, ""

def validate_password(password):
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must include at least one number."
    if not any(char.isupper() for char in password):
        return False, "Password must include at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must include at least one lowercase letter."
    return True, ""

def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            register_user(username, password)

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the dashboard.)")

                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()