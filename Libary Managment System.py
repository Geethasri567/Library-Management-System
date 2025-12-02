import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta
import csv
import os

USER_CSV = 'user.csv'

# Load users from CSV
def load_users():
    users = {}
    if os.path.exists(USER_CSV):
        with open(USER_CSV, 'r') as file:
            reader = csv.reader(file)
            try:
                next(reader)
                for row in reader:
                    if row:
                        users[row[0]] = row[1]
            except StopIteration:
                pass
    return users

# Save users to CSV
def save_users(users):
    with open(USER_CSV, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['username', 'password'])
        for username, password in users.items():
            writer.writerow([username, password])

# Books database
books = {
    "1984": {"author": "George Orwell", "status": "available", "no_of_copies": 5},
    "To Kill a Mockingbird": {"author": "Harper Lee", "status": "available", "no_of_copies": 5},
    "The Catcher in the Rye": {"author": "J.D. Salinger", "status": "available", "no_of_copies": 5},
    "Moby Dick": {"author": "Herman Melville", "status": "available", "no_of_copies": 5},
    "Pride and Prejudice": {"author": "Jane Austen", "status": "available", "no_of_copies": 5},
    "The Great Gatsby": {"author": "F. Scott Fitzgerald", "status": "available", "no_of_copies": 5},
    "The Hobbit": {"author": "J.R.R. Tolkien", "status": "available", "no_of_copies": 5},
    "Harry Potter and the Sorcerer's Stone": {"author": "J.K. Rowling", "status": "available", "no_of_copies": 5},
    "War and Peace": {"author": "Leo Tolstoy", "status": "available", "no_of_copies": 5},
    "Brave New World": {"author": "Aldous Huxley", "status": "available", "no_of_copies": 5}
}

# User class
class User:
    def __init__(self, user_id, username, password):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.borrowed_books = []

    def borrow_books(self, book_titles):
        messages = []
        for book_title in book_titles:
            book_title = book_title.strip()
            if book_title in books:
                if books[book_title]["no_of_copies"] > 0:
                    borrow_date = datetime.now()
                    return_date = borrow_date + timedelta(days=14)
                    self.borrowed_books.append({
                        "title": book_title,
                        "borrow_date": borrow_date,
                        "return_date": return_date
                    })
                    books[book_title]["no_of_copies"] -= 1
                    if books[book_title]["no_of_copies"] == 0:
                        books[book_title]["status"] = "borrowed"
                    messages.append(f"{book_title} borrowed. Return by {return_date.strftime('%Y-%m-%d')}")
                else:
                    messages.append(f"{book_title} is unavailable. Copies left: {books[book_title]['no_of_copies']}")
            else:
                messages.append(f"{book_title} not found.")
        return "\n".join(messages)

    def return_books(self, book_titles):
        messages = []
        for book_title in book_titles:
            book_title = book_title.strip()
            for borrowed_book in self.borrowed_books:
                if borrowed_book["title"] == book_title:
                    self.borrowed_books.remove(borrowed_book)
                    books[book_title]["no_of_copies"] += 1
                    books[book_title]["status"] = "available"
                    messages.append(f"{book_title} returned successfully.")
                    break
            else:
                messages.append(f"You have not borrowed {book_title}.")
        return "\n".join(messages)

    def display_checkouts(self):
        if not self.borrowed_books:
            return "No books borrowed."
        return "\n".join([f"'{book['title']}' (Return by: {book['return_date'].strftime('%Y-%m-%d')})"
                          for book in self.borrowed_books])

# Admin class
class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_book(self, title, author, copies):
        if title in books:
            return "Book already exists."
        books[title] = {"author": author, "status": "available", "no_of_copies": copies}
        return f"{title} by {author} added with {copies} copies."

    def add_more_copies(self, title, copies_to_add):
        if title in books:
            books[title]["no_of_copies"] += copies_to_add
            books[title]["status"] = "available"
            return f"Added {copies_to_add} copies of '{title}'. Total: {books[title]['no_of_copies']}."
        return "Book not found."

# Tkinter GUI
root = tk.Tk()
root.title("Library Management System")
root.geometry("750x500")

# Login screen
def show_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Login", font=("Helvetica", 16)).pack(pady=20)
    tk.Label(root, text="Username:").pack(pady=5)
    global user_entry
    user_entry = tk.Entry(root)
    user_entry.pack(pady=5)
    tk.Label(root, text="Password:").pack(pady=5)
    global password_entry
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    tk.Button(root, text="User Login", command=user_login).pack(pady=10)
    tk.Button(root, text="Admin Login", command=admin_login).pack(pady=10)
    tk.Button(root, text="Sign Up", command=sign_up).pack(pady=10)

# User login
def user_login():
    username = user_entry.get()
    password = password_entry.get()
    users = load_users()
    if username in users and users[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome {username}!")
        user_dashboard(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Admin login
def admin_login():
    username = user_entry.get()
    password = password_entry.get()
    if username == "admin" and password == "adminpassword":
        messagebox.showinfo("Login Successful", "Welcome Admin!")
        admin_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid admin credentials.")

# User dashboard
def user_dashboard(username):
    users = load_users()
    user = User(1, username, users[username])

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Welcome, {username}!", font=("Helvetica", 16)).pack(pady=20)
    tk.Label(root, text="Enter Book Title:").pack(pady=10)
    book_entry = tk.Entry(root, width=50)
    book_entry.pack(pady=10)

    def borrow():
        while True:
            book_title = book_entry.get().strip()
            if not book_title:
                messagebox.showwarning("Input Error", "Please enter a book title.")
                return

            if book_title not in books:
                messagebox.showerror("Error", f"{book_title} not found in library.")
                book_entry.delete(0, tk.END)
                return

            max_copies = books[book_title]['no_of_copies']
            if max_copies == 0:
                messagebox.showinfo("Unavailable", f"{book_title} is currently unavailable.")
                book_entry.delete(0, tk.END)
                return

            # Ask how many copies
            copies_needed = simpledialog.askinteger(
                "Copies", f"How many copies of '{book_title}' do you want? (Available: {max_copies})",
                minvalue=1, maxvalue=max_copies
            )
            if copies_needed is None:
                return

            messages = []
            for _ in range(copies_needed):
                msg = user.borrow_books([book_title])
                messages.append(msg)

            messagebox.showinfo("Borrowed Books", "\n".join(messages))
            book_entry.delete(0, tk.END)

            # Ask if user wants to borrow another book
            another = messagebox.askyesno("Borrow More", "Do you want to borrow another book?")
            if not another:
                break

    def return_b():
        titles = simpledialog.askstring("Return Books", "Enter book titles to return (comma-separated):")
        if titles:
            titles_list = titles.split(",")
            message = user.return_books(titles_list)
            messagebox.showinfo("Return Books", message)

    tk.Button(root, text="Borrow Books", command=borrow).pack(pady=5)
    tk.Button(root, text="Return Books", command=return_b).pack(pady=5)
    tk.Button(root, text="Display My Books", command=lambda: messagebox.showinfo("My Books", user.display_checkouts())).pack(pady=5)
    tk.Button(root, text="Logout", command=show_login_screen).pack(pady=20)

# Admin dashboard
def admin_dashboard():
    for widget in root.winfo_children():
        widget.destroy()
    tk.Label(root, text="Admin Dashboard", font=("Helvetica", 16)).pack(pady=20)

    def view_books():
        book_list = "\n".join([f"'{title}' by {details['author']} - {details['status']} (Copies: {details['no_of_copies']})"
                               for title, details in books.items()])
        messagebox.showinfo("Books in Library", book_list)

    def add_book():
        title = add_title_entry.get()
        author = add_author_entry.get()
        copies = int(add_copies_entry.get())
        result = Admin("admin", "adminpassword").add_book(title, author, copies)
        messagebox.showinfo("Add Book", result)

    def add_more():
        title = add_title_entry.get()
        copies = int(add_copies_entry.get())
        result = Admin("admin", "adminpassword").add_more_copies(title, copies)
        messagebox.showinfo("Add Copies", result)

    tk.Button(root, text="View Books", command=view_books).pack(pady=10)
    tk.Label(root, text="Book Title:").pack()
    add_title_entry = tk.Entry(root)
    add_title_entry.pack(pady=5)
    tk.Label(root, text="Author:").pack()
    add_author_entry = tk.Entry(root)
    add_author_entry.pack(pady=5)
    tk.Label(root, text="Copies:").pack()
    add_copies_entry = tk.Entry(root)
    add_copies_entry.pack(pady=5)

    tk.Button(root, text="Add Book", command=add_book).pack(pady=5)
    tk.Button(root, text="Add More Copies", command=add_more).pack(pady=5)
    tk.Button(root, text="Logout", command=show_login_screen).pack(pady=20)

# Sign up
def sign_up():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Sign Up", font=("Helvetica", 16)).pack(pady=20)
    tk.Label(root, text="Username:").pack(pady=5)
    sign_up_username_entry = tk.Entry(root)
    sign_up_username_entry.pack(pady=5)
    tk.Label(root, text="Password:").pack(pady=5)
    sign_up_password_entry = tk.Entry(root, show="*")
    sign_up_password_entry.pack(pady=5)

    def save_user():
        username = sign_up_username_entry.get()
        password = sign_up_password_entry.get()
        users = load_users()
        if username in users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            users[username] = password
            save_users(users)
            messagebox.showinfo("Success", "Signed up successfully!")
            show_login_screen()

    tk.Button(root, text="Sign Up", command=save_user).pack(pady=10)
    tk.Button(root, text="Back to Login", command=show_login_screen).pack(pady=5)

# Start the app
show_login_screen()
root.mainloop()
