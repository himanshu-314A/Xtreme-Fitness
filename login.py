import json


def load_users():
    try:
        with open("users.json", "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            return {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

users = load_users()

def signup():
    print("\n--- Sign Up ---")
    username = input("Enter a new username: ").strip()
    
    if username in users:
        print("Username already exists. Please choose another one.")
        return False
    
    password = input("Enter a new password: ").strip()
    users[username] = password
    save_users(users)
    print("Signup successful! You can now log in.")
    return True

def login():
    print("\n--- Log In ---")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    
    if username in users and users[username] == password:
        print(f"Login successful! Welcome back, {username}.")
    else:
        print("Login failed! Incorrect username or password.")

def main():
    print("Welcome!")
    while True:
        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == '1':
            if signup():
                login()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
