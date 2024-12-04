import os
import hashlib
import csv
from datetime import datetime
import getpass

user_record = "users.txt"

expenses = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    username = input("\nEnter your Username: ")
    password = getpass.getpass("Enter your Password: ")

    if user_exists(username):
        print("Username already exists. Please choose another.")
        return
    hashed_password = hash_password(password)

    with open(user_record, 'a') as file:
        file.write(f"{username},{hashed_password}\n")
    
    print("User successfully registered!")

def login_user():
    username = input("\nEnter your Username: ")
    password = getpass.getpass("Enter your Password: ")

    if authenticate_user(username, password):
        load_records_to_dict(username) 
        print("Login Successful!")
        return username
    else:
        print("Invalid username or password.")
        return None

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
    date = input(f"Enter date (YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')

    new_record = {
        'Date': date,
        'Amount': amount,
        'Category': category,
        'Type': record_type
    }
    expenses[username].append(new_record)
    save_dict_to_csv(username)
    print("Record added successfully!")

def read_records(username):
    if not expenses[username]:
        print("No records found.")
        return
    print("\n----------- Expense Records -----------")
    for record in expenses[username]:
        print(f"""
          Date: {record['Date']}
          Amount: {record['Amount']}
          Category: {record['Category']}
          Type: {record['Type']}
""")
        
def update_record(username):
    date_to_update = input("Enter the date of the record to update (YYYY-MM-DD): ")
    updated = False

    for record in expenses[username]:
        if record['Date'] == date_to_update:
            print(f"Record found: {record}")
            record['Amount'] = float(input("Enter new amount: "))
            record['Category'] = input("Enter new category: ")
            record['Type'] = input("Enter new record type (income/expense): ").lower()
            updated = True
            break

    if updated:
        save_dict_to_csv(username)
        print(f"Record for {date_to_update} updated.")
    else:
        print(f"No record found for {date_to_update}.")

def delete_record(username):
    date_to_delete = input("Enter the date of the record to delete (YYYY-MM-DD): ")
    initial_length = len(expenses[username])
    expenses[username] = [record for record in expenses[username] if record['Date'] != date_to_delete]

    if len(expenses[username]) < initial_length:
        save_dict_to_csv(username)
        print(f"Record for {date_to_delete} deleted.")
    else:
        print(f"No record found for {date_to_delete}.")

def view_reports(username):
    total_income = sum(float(record['Amount']) for record in expenses[username] if record['Type'] == 'income')
    total_expense = sum(float(record['Amount']) for record in expenses[username] if record['Type'] == 'expense')
    balance = total_income - total_expense
    print("\n----------- Expense Report -----------")
    print(f"\tTotal Income: {total_income}")
    print(f"\tTotal Expenses: {total_expense}")
    print(f"\tBalance: {balance}\n")
    
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
  if not username:
      login_user()
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
