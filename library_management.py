import json
import datetime
import random
import os

# PERSON CLASS
class Person:
    def __init__(self, name):
        self.name = name.title()

# MEMBER CLASS
class Member(Person):
    def __init__(self, name, member_id):
        super().__init__(name)
        self.member_id = member_id
        self.borrowed_books = []

# LIBRARIAN CLASS
class Librarian(Person):
    def __init__(self, name):
        super().__init__(name)

    def add_book(self, library):
        title = input("Enter book name: ").strip().title()
        author = input("Enter author name: ").strip().title()
        price = float(input("Enter book price: ").strip())
        copies = int(input("Enter available copies: ").strip())
        
        if title not in library.books:
            library.books[title] = {'author': author, 'price': price, 'available_copies': copies}
            library.save_data()
            print(f"Book '{title}' by {author} added to library.")
        else:
            print(f"'{title}' already exists in the library.")
            
    def update_book(self, library):
        title = input("Enter book name to update: ").strip().title()
        if title in library.books:
            print("1. Update Price\n2. Update Available Copies")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                new_price = float(input("Enter new price: ").strip())
                library.books[title]['price'] = new_price
                print(f"Price of '{title}' updated to {new_price}.")
            elif choice == '2':
                new_copies = int(input("Enter new available copies: ").strip())
                library.books[title]['available_copies'] = new_copies
                print(f"Available copies of '{title}' updated to {new_copies}.")
            else:
                print(f"Invalid choice!")
            library.save_data()
        else:
            print(f"'{title}' not found in the library.")

# Library Class
class Library:
    def __init__(self, book_file='books.json', member_file='members.json'):
        self.books = {}
        self.members = {}
        self.transactions = []
        self.book_file = book_file
        self.member_file = member_file
        self.load_data()

    def save_data(self):
        with open(self.book_file, 'w') as file:
            json.dump(self.books, file, indent=4)
        with open(self.member_file, 'w') as file:
            json.dump({name: {'member_id': member.member_id, 'borrowed_books': member.borrowed_books} for name, member in self.members.items()}, file, indent=4)
        with open('transactions.json', 'w') as file:
            json.dump(self.transactions, file, indent=4)
        print("Library data saved.")

    def load_data(self):
        if os.path.exists(self.book_file):
            with open(self.book_file, 'r') as file:
                self.books = json.load(file)
        if os.path.exists(self.member_file):
            with open(self.member_file, 'r') as file:
                member_data = json.load(file)
                for name, details in member_data.items():
                    self.members[name] = Member(name, details['member_id'])
                    self.members[name].borrowed_books = details['borrowed_books']
        if os.path.exists('transactions.json'):
            with open('transactions.json', 'r') as file:
                self.transactions = json.load(file)

    def register_member(self):
        print(" Register a new member:")
        name = input("Enter your name: ").strip().title()
        if name in self.members:
            print(f"⚠ '{name}' is already registered. Please log in.")
            return None
        member_id = random.randint(1000, 9999)
        self.members[name] = Member(name, member_id)
        self.save_data()
        print(f"✔ Registration successful! '{name}' is registered with ID: {member_id}.")
        return name

    def login_member(self):
        print(" Member Login:")
        name = input("Enter your name: ").strip().title()
        if name in self.members:
            print(f"✔ Login successful! Welcome back, {name}.")
            return name
        else:
            print(f"✖ User '{name}' not found. Please register first.")
            return None
        
    def display_books(self):
        print("\n Library Books:")
        if self.books:
            print(f"{'Title':<30} {'Author':<20} {'Price ($)':<10} {'Available Copies':<10}")
            print("-" * 75)
            for title, details in self.books.items():
                print(f"{title:<30} {details['author']:<20} {details['price']:<10.2f} {details['available_copies']:<10}")
        else:
             print(f"✖ No books available in the library.")
    
    def issue_book(self, member_name):
        book_name = input("Enter book name to borrow: ").strip().title()
        if book_name in self.books and self.books[book_name]['available_copies'] > 0:
            self.books[book_name]['available_copies'] -= 1
            self.members[member_name].borrowed_books.append(book_name)
            transaction = {'member': member_name, 'book': book_name, 'type': 'Issue', 'date': str(datetime.datetime.now())}
            self.transactions.append(transaction)
            self.save_data()
            print(f"Book '{book_name}' issued to {member_name}.")
        else:
            print(f"Book '{book_name}' is not available.")

    def return_book(self, member_name):
        book_name = input("Enter book name to return: ").strip().title()
        if book_name in self.members[member_name].borrowed_books:
            self.members[member_name].borrowed_books.remove(book_name)
            self.books[book_name]['available_copies'] += 1
            transaction = {'member': member_name, 'book': book_name, 'type': 'Return', 'date': str(datetime.datetime.now())}
            self.transactions.append(transaction)
            self.save_data()
            print(f"Book '{book_name}' returned by {member_name}.")
        else:
            print(f"You have not borrowed '{book_name}'.")

    def purchase_book(self, member_name):
        book_name = input("Enter book name to purchase: ").strip().title()
        if book_name in self.books:
            price = self.books[book_name]['price']
            transaction = {'member': member_name, 'book': book_name, 'type': 'Purchase', 'date': str(datetime.datetime.now()), 'price': price}
            self.transactions.append(transaction)
            self.save_data()
            print(f"Book '{book_name}' purchased for ${price:.2f}.")
            self.books[book_name]['available_copies'] -= 1 
        else:
            print(f"Book '{book_name}' not found.")

    def display_transactions(self):
        print(f" Transactions:")
        if self.transactions:
            for transaction in self.transactions:
                print(f"{transaction}")
        else:
            print(f"No transactions available.")

    def logout_member(self, member_name):
        print(f"Logging out {member_name}.")
        return None

# Initialize library and librarian
library = Library()
librarian = Librarian("Alice")

# User Authentication
while True:
    print(f"\n Library System")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    
    auth_choice = input("Enter your choice: ").strip()

    if auth_choice == '1':
        user_name = library.register_member()
        if user_name:
            user_name = library.login_member()
            if user_name:
                break
    elif auth_choice == '2':
        user_name = library.login_member()
        if user_name:
            break
    elif auth_choice == '3':
        print(f" Exiting Library System. Goodbye!")
        exit()
    else:
        print(f" Invalid choice! Please enter 1, 2, or 3.")

# Main Menu
while True:
    print(f"\nLibrary System")
    print("1. Add Book")
    print("2. Update Book")
    print("3. Display Books")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Purchase Book")
    print("7. Display Transactions")
    print("8. Logout member")
    print("9. Exit")

    choice = input("Enter your choice: ").strip()
    
    if choice == '1':
        librarian.add_book(library)
    elif choice == '2':
        librarian.update_book(library)
    elif choice == '3':
        library.display_books()
    elif choice == '4':
        library.issue_book(user_name)
    elif choice == '5':
        library.return_book(user_name)
    elif choice == '6':
        library.purchase_book(user_name)
    elif choice == '7':
        library.display_transactions()
    elif choice == '8':
        user_name = library.logout_member(user_name)
        while True:
            print(f"\n Library System")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            
            auth_choice = input("Enter your choice: ").strip()

           
