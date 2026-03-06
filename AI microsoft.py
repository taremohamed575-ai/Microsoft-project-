import json
import os
import getpass

DB_FILE = 'database.json'

def load_data():
    """Loads users data from the JSON file."""
    # Check if the file exists
    if not os.path.exists(DB_FILE):
        return {}
    
    try:
        # Load the data from the JSON file
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(users):
    """Saves the users dictionary back to the JSON file in real-time."""
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def register_user():
    """Handles new user registration."""
    print("\n--- Register ---")
    username = input("Enter a new username: ").strip()
    
    if not username:
        print("Error: Username cannot be empty.")
        return

    users = load_data()
    
    # Validate that the username isn't taken
    if username in users:
        print("Error: Username already exists! Please choose another one.")
        return
        
    password = getpass.getpass("Enter a secure password: ")
    if not password:
        print("Error: Password cannot be empty.")
        return

    try:
        initial_balance = float(input("Enter initial balance: "))
        if initial_balance < 0:
            print("Error: Initial balance cannot be negative.")
            return
    except ValueError:
        print("Error: Invalid amount. Please enter a numerical value.")
        return

    # Add the new user to the data
    users[username] = {
        "password": password,
        "balance": initial_balance
    }
    
    # Save the updated data back to DB
    save_data(users)
    print(f"Success: Account created for '{username}' with a balance of ${initial_balance:.2f}!")

def login_user():
    """Validates credentials and returns the logged-in username."""
    print("\n--- Login ---")
    username = input("Enter username: ").strip()
    password = getpass.getpass("Enter password: ")

    users = load_data()

    # Verify if credentials match the database
    if username in users and users[username]["password"] == password:
        print(f"Success: Welcome back, {username}!")
        return username
    else:
        print("Error: Invalid username or password.")
        return None

def view_balance(username):
    """Displays the user's current balance."""
    users = load_data()
    balance = users[username]["balance"]
    print(f"Current Balance for {username}: ${balance:.2f}")

def deposit(username, amount):
    """Adds funds to the user's balance."""
    if amount <= 0:
        print("Error: Deposit amount must be greater than zero.")
        return

    users = load_data()
    # Perform calculation
    users[username]["balance"] += amount
    # Save the updated data
    save_data(users)
    print(f"Success: ${amount:.2f} deposited to your account.")

def withdraw(username, amount):
    """Deducts funds from the user's balance if sufficient."""
    if amount <= 0:
        print("Error: Withdrawal amount must be greater than zero.")
        return

    users = load_data()
    
    # Verify conditions
    if users[username]["balance"] < amount:
        print("Error: Insufficient funds!")
        return

    # Perform calculation
    users[username]["balance"] -= amount
    # Save the updated data
    save_data(users)
    print(f"Success: ${amount:.2f} withdrawn from your account.")

def transfer(sender_username, receiver_username, amount):
    """Transfers funds from the sender to the receiver."""
    if sender_username == receiver_username:
        print("Error: You cannot transfer money to yourself.")
        return

    if amount <= 0:
        print("Error: Transfer amount must be greater than zero.")
        return

    users = load_data()
    
    # Verify conditions: receiver exists
    if receiver_username not in users:
        print(f"Error: User '{receiver_username}' does not exist.")
        return

    # Verify conditions: sender has enough balance
    if users[sender_username]["balance"] < amount:
        print("Error: Insufficient funds for this transfer!")
        return

    # Perform calculations
    users[sender_username]["balance"] -= amount
    users[receiver_username]["balance"] += amount
    # Save the updated data
    save_data(users)
    print(f"Success: ${amount:.2f} transferred to {receiver_username}.")

def dashboard(username):
    """Displays the user dashboard once logged in."""
    while True:
        print(f"\n=== Dashboard: {username} ===")
        print("1. View Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Logout")
        
        choice = input("Select an option (1-5): ").strip()

        if choice == '1':
            view_balance(username)
            
        elif choice == '2':
            try:
                amt = float(input("Enter amount to deposit: "))
                deposit(username, amt)
            except ValueError:
                print("Error: Invalid amount. Please enter a numerical value.")
                
        elif choice == '3':
            try:
                amt = float(input("Enter amount to withdraw: "))
                withdraw(username, amt)
            except ValueError:
                print("Error: Invalid amount. Please enter a numerical value.")
                
        elif choice == '4':
            recipient = input("Enter recipient's username: ").strip()
            try:
                amt = float(input(f"Enter amount to transfer to {recipient}: "))
                transfer(username, recipient, amt)
            except ValueError:
                print("Error: Invalid amount. Please enter a numerical value.")
                
        elif choice == '5':
            print(f"Logging out {username}...")
            break
            
        else:
            print("Error: Invalid option. Please choose 1-5.")

def main():
    """Main Menu Flow"""
    while True:
        print("\n=== Main Menu ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            register_user()
        elif choice == '2':
            user = login_user()
            if user:
                dashboard(user)
        elif choice == '3':
            print("Exiting. Goodbye!")
            break
        else:
            print("Error: Invalid option. Please choose 1-3.")

if __name__ == "__main__":
    main()
