import csv
from datetime import datetime

# File paths for the CSV files
BOOKS_FILE = 'books.csv'
USERS_FILE = 'users.csv'


# Function to read CSV file into a list of dictionaries
def read_csv(file):
    with open(file, mode='r') as f:
        return list(csv.DictReader(f))


# Function to write data to CSV file
def write_csv(file, data, fieldnames):
    with open(file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Function to display all books
def display_books():
    books = read_csv(BOOKS_FILE)
    print("Available books:")
    for book in books:
        status = 'Available' if book['Available'] == '1' else 'Issued'
        print(f"ID: {book['BookID']}, Title: {book['Title']}, Author: {book['Author']}, Status: {status}")


# Function to check if a book is available
def check_availability(book_id):
    books = read_csv(BOOKS_FILE)
    for book in books:
        if book['BookID'] == book_id:
            return book['Available'] == '1'
    return False


# Function to issue a book
def issue_book(book_id, user_id):
    books = read_csv(BOOKS_FILE)
    users = read_csv(USERS_FILE)

    # Format user_id to have leading zeros
    #user_id = str(user_id).zfill(3)  # Assuming User IDs are 3 digits long

    # Debug: Print out all users to verify IDs
    print(f"Entered User ID: '{user_id}'")
    print("Existing Users in System:")
    for user in users:
        print(f"UserID: '{user['UserID']}' - Name: {user['Name']}")

    if not check_availability(book_id):
        print("Book is not available.")
        return

    # Update book availability
    book_updated = False
    for book in books:
        if book['BookID'] == book_id:
            book['Available'] = '0'
            book['IssuedTo'] = user_id
            book['IssueDate'] = datetime.now().strftime('%Y-%m-%d')
            book_updated = True

    if not book_updated:
        print("Book ID not found.")
        return

    # Update user record
    user_updated = False
    for user in users:
        print(f"Comparing with UserID: '{user['UserID']}'")
        if user['UserID'] == user_id:
            print(f"Updating user: {user['Name']} with ID: {user_id}")
            user['IssuedBookID'] = book_id
            user['IssueDate'] = datetime.now().strftime('%Y-%m-%d')
            user_updated = True

    if not user_updated:
        print("User ID not found in system.")
        return

    # Write updates to the CSV files
    write_csv(BOOKS_FILE, books, fieldnames=books[0].keys())
    write_csv(USERS_FILE, users, fieldnames=users[0].keys())

    print(f"Book ID {book_id} has been issued to User ID {user_id}.")

def return_book(book_id, user_id):
    books = read_csv(BOOKS_FILE)
    users = read_csv(USERS_FILE)

    # Format user_id to have leading zeros
    #user_id = str(user_id).zfill(3)  # Assuming User IDs are 3 digits long

    # Debug: Print out all users to verify IDs
    print(f"Entered User ID: '{user_id}'")
    print("Existing Users in System:")
    for user in users:
        print(f"UserID: '{user['UserID']}' - Name: {user['Name']}")

    # Update book availability
    book_updated = False
    for book in books:
        if book['BookID'] == book_id and book['IssuedTo'] == user_id:
            book['Available'] = '1'
            book['IssuedTo'] = ''
            book['IssueDate'] = ''
            book['ReturnDate'] = datetime.now().strftime('%Y-%m-%d')
            book_updated = True

    if not book_updated:
        print("Book or User ID not found for return.")
        return

    # Update user record
    user_updated = False
    for user in users:
        if user['UserID'] == user_id and user['IssuedBookID'] == book_id:
            print(f"Updating return for user: {user['Name']} with ID: {user_id}")
            user['IssuedBookID'] = ''
            user['IssueDate'] = ''
            user['ReturnDate'] = datetime.now().strftime('%Y-%m-%d')
            user_updated = True

    if not user_updated:
        print("User ID not found or mismatch.")
        return

    # Write updates to the CSV files
    write_csv(BOOKS_FILE, books, fieldnames=books[0].keys())
    write_csv(USERS_FILE, users, fieldnames=users[0].keys())

    print(f"Book ID {book_id} has been returned by User ID {user_id}.")

# Main menu to interact with the system
def main_menu():
    while True:
        print("\nLibrary Management System")
        print("1. Display all books")
        print("2. Check availability of a book")
        print("3. Issue a book")
        print("4. Return a book")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            display_books()
        elif choice == '2':
            book_id = input("Enter Book ID: ")
            if check_availability(book_id):
                print(f"Book ID {book_id} is available.")
            else:
                print(f"Book ID {book_id} is not available.")
        elif choice == '3':
            book_id = input("Enter Book ID: ")
            user_id = input("Enter User ID: ")
            issue_book(book_id, user_id)
        elif choice == '4':
            book_id = input("Enter Book ID: ")
            user_id = input("Enter User ID: ")
            return_book(book_id, user_id)
        elif choice == '5':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")

main_menu()