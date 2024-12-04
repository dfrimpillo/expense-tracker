import os
import hashlib
import csv
from datetime import datetime

user_record = "users.txt"

expenses = {}
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    username = input("\nEnter your Username: ")
    password = input("Enter your Password: ")

    if user_exists(username):
        print("Username already exists. Please choose another.")
        return
    hashed_password = hash_password(password)

    with open(user_record, 'a') as file:
        file.write(f"{username},{hashed_password}\n")
    
    print("User successfully registered!")

def login_user():
    username = input("\nEnter your Username: ")
    password = input("Enter your Password: ")

    if authenticate_user(username, password):
        load_records_to_dict(username) 
        print("Login Successful!")
        return username
    else:
        print("Invalid username or password.")

def user_exists(username):
    if not os.path.exists(user_record):
        return False
    
    with open(user_record, 'r') as file:
        users = file.readlines()
    
    for user in users:
        saved_username, _ = user.strip().split(',')
        if saved_username == username:
            return True
    return False

def authenticate_user(username, password):
    if not os.path.exists(user_record):
        return False
    
    with open(user_record, 'r') as file:
        users = file.readlines()
    
    hashed_password = hash_password(password)

    for user in users:
        saved_username, saved_password = user.strip().split(',')
        if saved_username == username and saved_password == hashed_password:
            return True
    
    return False

def load_records_to_dict(username):
    file_path = f"{username}_expenses.csv"
    expenses[username] = []  
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            expenses[username] = list(reader)

def save_dict_to_csv(username):
    file_path = f"{username}_expenses.csv"
    with open(file_path, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Date', 'Amount', 'Category', 'Description', 'Type'])
        writer.writeheader()
        writer.writerows(expenses[username])

def create_record(username):
    record_type = input("Enter record type (income/expense): ").lower()
    amount = float(input("Enter amount: "))
    category = input("Enter category (e.g., food, rent, salary): ")
    description = input("Enter description: ")
    date = input(f"Enter date (YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    new_record = {
        'Date': date,
        'Amount': amount,
        'Category': category,
        'Description': description,
        'Type': record_type
    }
    expenses[username].append(new_record)
    save_dict_to_csv(username)
    print("Record added successfully!")

def read_records(username):
    if not expenses[username]:
        print("No records found.")
        return
    print("\n▒▒▒▒▒▒▒▒▒▒▒▒ Expense Records ▒▒▒▒▒▒▒▒▒▒▒▒")
    for record in expenses[username]:
        print(f"""
          Date: {record['Date']}
          Amount: {record['Amount']}
          Category: {record['Category']}
          Description: {record['Description']}
          Type: {record['Type']}
""")
def main_menu():
  print("▒"*42)
  print("▒▒\t                           \t▒▒")
  print("▒▒\tWelcome to Expense Tracker!\t▒▒")
  print("▒▒\t                           \t▒▒")
  print("▒"*42)

  choice = input("\nDo you have an account? (y/n): ").lower()

  if choice == 'n':
    r_choice = input("Would you like to register? (y/n): ").lower()
    if r_choice == 'y':
            register_user()
    elif choice == 'y':
        login_user()
    else:
        print("Invalid choice.")
  print("\nEnter your login details:")
  username = login_user()

  while True: 
      print("▒"*42)
      print("▒▒\t                           \t▒▒")
      print("▒▒\t\tExpense Tracker\t\t▒▒")
      print("▒▒\t1. Add Record (Income/Expense)\t▒▒")
      print("▒▒\t2. View All Records\t\t▒▒")
      print("▒▒\t3. Update Record\t\t▒▒")
      print("▒▒\t4. Delete Record\t\t▒▒")
      print("▒▒\t5. View Reports\t\t\t▒▒")
      print("▒▒\t6. Logout\t\t\t▒▒")
      print("▒▒\t                           \t▒▒")
      print("▒"*42)
      
      choice = input("Choose an option: ")

      if choice == '1':
          create_record(username)
      elif choice == '2':
          read_records(username)
      elif choice == '3':
          update_record(username)
      elif choice == '4':
          delete_record(username)
      elif choice == '5':
          view_reports(username)
      elif choice == '6':
          print("Logged out successfully.")
          break
      else:
            print("Invalid option, try again.")
if __name__ == "__main__":
    main_menu()
