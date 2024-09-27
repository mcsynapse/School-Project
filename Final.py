import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkcalendar import DateEntry
from datetime import datetime

# Initialize Database
def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS book (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        isbn TEXT,
                        genre TEXT,
                        publication_date TEXT,
                        language TEXT,
                        bookshelf_no TEXT,
                        rack_no TEXT,
                        unique_book_id TEXT UNIQUE,
                        availability BOOLEAN)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS admins (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        class TEXT,
                        roll_no TEXT,
                        admission_no TEXT,
                        unique_card_no TEXT UNIQUE)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS lend (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        book_id TEXT,
                        card_no TEXT,
                        lend_date TEXT,
                        due_date TEXT,
                        return_date TEXT,
                        fine INTEGER)''')

    # Check if the admin table is empty, if so, add default admin
    cursor.execute('SELECT COUNT(*) FROM admins')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''INSERT INTO admins (username, password) VALUES (?, ?)''',
                       ('admin', 'admin123'))

    conn.commit()
    conn.close()

init_db()

def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admins WHERE username = ? AND password = ?', (username, password))
    result = cursor.fetchone()
    
    if result:
        main_page()
    else:
        messagebox.showerror("Error", "Invalid credentials")
    
    conn.close()

def main_page():
    login_window.destroy()
    main = tk.Tk()
    main.title("Library Management System")

    buttons = ["ADD BOOK", "EDIT BOOK", "DELETE BOOK", "FETCH BOOK DETAILS", "CHECK BOOK AVAILABILITY",
               "ADD STUDENT", "LEND BOOK", "RETURN BOOK", "ADD ADMIN", "FETCH STUDENT DETAILS"]
    
    functions = [add_book, edit_book, delete_book, fetch_book_details, check_book_availability,
                 add_student, lend_book, return_book, add_admin, fetch_student_details]
    
    for btn_text, func in zip(buttons, functions):
        btn = tk.Button(main, text=btn_text, font=("Arial", 14), bg="lightblue", command=func)
        btn.pack(pady=10, fill=tk.X)

    main.mainloop()

def add_book():
    def submit_book():
        title = entry_title.get()
        author = entry_author.get()
        isbn = entry_isbn.get()
        genre = entry_genre.get()
        pub_date = entry_pub_date.get()
        language = entry_language.get()
        bookshelf_no = entry_bookshelf_no.get()
        rack_no = entry_rack_no.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(id) FROM book')
        max_id = cursor.fetchone()[0]
        book_id = f"{(max_id or 0) + 1:05d}"
        
        cursor.execute('''INSERT INTO book (title, author, isbn, genre, publication_date, language, bookshelf_no, 
                          rack_no, unique_book_id, availability) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (title, author, isbn, genre, pub_date, language, bookshelf_no, rack_no, book_id, True))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Book added with ID: {book_id}")
        add_book_window.destroy()

    add_book_window = tk.Toplevel()
    add_book_window.title("Add Book")
    
    labels = ["Title", "Author", "ISBN", "Genre", "Publication Date", "Language", "Bookshelf No.", "Rack No."]
    entries = []
    
    for label in labels:
        tk.Label(add_book_window, text=label, font=("Arial", 12)).pack(pady=5)
        entry = tk.Entry(add_book_window, font=("Arial", 12))
        entry.pack(pady=5)
        entries.append(entry)
    
    entry_title, entry_author, entry_isbn, entry_genre, entry_pub_date, entry_language, entry_bookshelf_no, entry_rack_no = entries
    
    tk.Button(add_book_window, text="Submit", font=("Arial", 12), command=submit_book).pack(pady=20)

def edit_book():
    def fetch_book():
        book_id = entry_book_id.get()
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM book WHERE unique_book_id = ?', (book_id,))
        book = cursor.fetchone()
        
        if book:
            entry_title.delete(0, tk.END)
            entry_author.delete(0, tk.END)
            entry_isbn.delete(0, tk.END)
            entry_genre.delete(0, tk.END)
            entry_pub_date.delete(0, tk.END)
            entry_language.delete(0, tk.END)
            entry_bookshelf_no.delete(0, tk.END)
            entry_rack_no.delete(0, tk.END)
            
            entry_title.insert(0, book[1])
            entry_author.insert(0, book[2])
            entry_isbn.insert(0, book[3])
            entry_genre.insert(0, book[4])
            entry_pub_date.insert(0, book[5])
            entry_language.insert(0, book[6])
            entry_bookshelf_no.insert(0, book[7])
            entry_rack_no.insert(0, book[8])
            
        else:
            messagebox.showerror("Error", "Book not found")
        conn.close()
    
    def update_book():
        book_id = entry_book_id.get()
        title = entry_title.get()
        author = entry_author.get()
        isbn = entry_isbn.get()
        genre = entry_genre.get()
        pub_date = entry_pub_date.get()
        language = entry_language.get()
        bookshelf_no = entry_bookshelf_no.get()
        rack_no = entry_rack_no.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE book SET title = ?, author = ?, isbn = ?, genre = ?, publication_date = ?, language = ?, 
                          bookshelf_no = ?, rack_no = ? WHERE unique_book_id = ?''',
                       (title, author, isbn, genre, pub_date, language, bookshelf_no, rack_no, book_id))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Book ID: {book_id} updated successfully")
        edit_book_window.destroy()
    
    edit_book_window = tk.Toplevel()
    edit_book_window.title("Edit Book")
    
    tk.Label(edit_book_window, text="Book ID", font=("Arial", 12)).pack(pady=5)
    entry_book_id = tk.Entry(edit_book_window, font=("Arial", 12))
    entry_book_id.pack(pady=5)
    tk.Button(edit_book_window, text="Fetch Book", font=("Arial", 12), command=fetch_book).pack(pady=5)
    
    labels = ["Title", "Author", "ISBN", "Genre", "Publication Date", "Language", "Bookshelf No.", "Rack No."]
    entries = []
    
    for label in labels:
        tk.Label(edit_book_window, text=label, font=("Arial", 12)).pack(pady=5)
        entry = tk.Entry(edit_book_window, font=("Arial", 12))
        entry.pack(pady=5)
        entries.append(entry)
    
    entry_title, entry_author, entry_isbn, entry_genre, entry_pub_date, entry_language, entry_bookshelf_no, entry_rack_no = entries
    
    tk.Button(edit_book_window, text="Update Book", font=("Arial", 12), command=update_book).pack(pady=20)

def delete_book():
    def remove_book():
        book_id = entry_book_id.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM book WHERE unique_book_id = ?', (book_id,))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Book ID: {book_id} deleted successfully")
        delete_book_window.destroy()

    delete_book_window = tk.Toplevel()
    delete_book_window.title("Delete Book")
    
    tk.Label(delete_book_window, text="Book ID", font=("Arial", 12)).pack(pady=5)
    entry_book_id = tk.Entry(delete_book_window, font=("Arial", 12))
    entry_book_id.pack(pady=5)
    tk.Button(delete_book_window, text="Delete Book", font=("Arial", 12), command=remove_book).pack(pady=20)

def fetch_book_details():
    def display_book():
        book_id = entry_book_id.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM book WHERE unique_book_id = ?', (book_id,))
        book = cursor.fetchone()
        
        if book:
            result = f"Title: {book[1]}\nAuthor: {book[2]}\nISBN: {book[3]}\nGenre: {book[4]}\nPublication Date: {book[5]}\nLanguage: {book[6]}\nBookshelf No.: {book[7]}\nRack No.: {book[8]}\nAvailability: {'Yes' if book[10] else 'No'}"
            messagebox.showinfo("Book Details", result)
        else:
            messagebox.showerror("Error", "Book not found")
        
        conn.close()
    
    fetch_book_details_window = tk.Toplevel()
    fetch_book_details_window.title("Fetch Book Details")
    
    tk.Label(fetch_book_details_window, text="Book ID", font=("Arial", 12)).pack(pady=5)
    entry_book_id = tk.Entry(fetch_book_details_window, font=("Arial", 12))
    entry_book_id.pack(pady=5)
    tk.Button(fetch_book_details_window, text="Fetch Details", font=("Arial", 12), command=display_book).pack(pady=20)

def check_book_availability():
    def check_availability():
        book_id = entry_book_id.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT availability FROM book WHERE unique_book_id = ?', (book_id,))
        availability = cursor.fetchone()
        
        if availability:
            messagebox.showinfo("Book Availability", f"Book ID: {book_id} is {'available' if availability[0] else 'not available'}")
        else:
            messagebox.showerror("Error", "Book not found")
        
        conn.close()
    
    check_book_availability_window = tk.Toplevel()
    check_book_availability_window.title("Check Book Availability")
    
    tk.Label(check_book_availability_window, text="Book ID", font=("Arial", 12)).pack(pady=5)
    entry_book_id = tk.Entry(check_book_availability_window, font=("Arial", 12))
    entry_book_id.pack(pady=5)
    tk.Button(check_book_availability_window, text="Check Availability", font=("Arial", 12), command=check_availability).pack(pady=20)

def add_student():
    def submit_student():
        name = entry_name.get()
        student_class = entry_class.get()
        roll_no = entry_roll_no.get()
        admission_no = entry_admission_no.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(id) FROM students')
        max_id = cursor.fetchone()[0]
        card_no = f"{(max_id or 0) + 1:05d}"
        
        cursor.execute('''INSERT INTO students (name, class, roll_no, admission_no, unique_card_no) 
                          VALUES (?, ?, ?, ?, ?)''',
                       (name, student_class, roll_no, admission_no, card_no))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Student added with Card No: {card_no}")
        add_student_window.destroy()

    add_student_window = tk.Toplevel()
    add_student_window.title("Add Student")
    
    labels = ["Name", "Class", "Roll No.", "Admission No."]
    entries = []
    
    for label in labels:
        tk.Label(add_student_window, text=label, font=("Arial", 12)).pack(pady=5)
        entry = tk.Entry(add_student_window, font=("Arial", 12))
        entry.pack(pady=5)
        entries.append(entry)
    
    entry_name, entry_class, entry_roll_no, entry_admission_no = entries
    
    tk.Button(add_student_window, text="Submit", font=("Arial", 12), command=submit_student).pack(pady=20)



def lend_book():
    def submit_lend():
        book_id = entry_book_id.get()
        card_no = entry_card_no.get()
        lend_date = entry_lend_date.get_date().strftime('%Y-%m-%d')
        due_date = entry_due_date.get_date().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(id) FROM lend')
        max_id = cursor.fetchone()[0]
        lend_id = f"{(max_id or 0) + 1:05d}"
        
        cursor.execute('''INSERT INTO lend (book_id, card_no, lend_date, due_date) 
                          VALUES (?, ?, ?, ?)''',
                       (book_id, card_no, lend_date, due_date))
        cursor.execute('UPDATE book SET availability = ? WHERE unique_book_id = ?', (False, book_id))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Lend recorded with Lend ID: {lend_id}")
        lend_book_window.destroy()

    lend_book_window = tk.Toplevel()
    lend_book_window.title("Lend Book")
    
    tk.Label(lend_book_window, text="Book ID", font=("Arial", 12)).pack(pady=5)
    entry_book_id = tk.Entry(lend_book_window, font=("Arial", 12))
    entry_book_id.pack(pady=5)
    
    tk.Label(lend_book_window, text="Card No.", font=("Arial", 12)).pack(pady=5)
    entry_card_no = tk.Entry(lend_book_window, font=("Arial", 12))
    entry_card_no.pack(pady=5)
    
    tk.Label(lend_book_window, text="Lend Date", font=("Arial", 12)).pack(pady=5)
    entry_lend_date = DateEntry(lend_book_window, font=("Arial", 12), date_pattern='y-mm-dd')
    entry_lend_date.pack(pady=5)
    
    tk.Label(lend_book_window, text="Due Date", font=("Arial", 12)).pack(pady=5)
    entry_due_date = DateEntry(lend_book_window, font=("Arial", 12), date_pattern='y-mm-dd')
    entry_due_date.pack(pady=5)
    
    tk.Button(lend_book_window, text="Submit", font=("Arial", 12), command=submit_lend).pack(pady=20)

def return_book():
    def submit_return():
        lend_id = entry_lend_id.get()
        return_date = entry_return_date.get_date().strftime('%Y-%m-%d')
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT lend_date, due_date, book_id FROM lend WHERE id = ?', (lend_id,))
        lend_record = cursor.fetchone()
        
        if lend_record:
            lend_date = datetime.strptime(lend_record[0], '%Y-%m-%d')
            due_date = datetime.strptime(lend_record[1], '%Y-%m-%d')
            return_date_dt = datetime.strptime(return_date, '%Y-%m-%d')
            book_id = lend_record[2]
            
            fine = max((return_date_dt - due_date).days, 0) * 5
            cursor.execute('UPDATE lend SET return_date = ?, fine = ? WHERE id = ?', (return_date, fine, lend_id))
            cursor.execute('UPDATE book SET availability = ? WHERE unique_book_id = ?', (True, book_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Book returned with fine: Rs {fine}")
            return_book_window.destroy()
        else:
            messagebox.showerror("Error", "Lend ID not found")
            conn.close()

    return_book_window = tk.Toplevel()
    return_book_window.title("Return Book")
    
    tk.Label(return_book_window, text="Lend ID", font=("Arial", 12)).pack(pady=5)
    entry_lend_id = tk.Entry(return_book_window, font=("Arial", 12))
    entry_lend_id.pack(pady=5)
    
    tk.Label(return_book_window, text="Return Date", font=("Arial", 12)).pack(pady=5)
    entry_return_date = DateEntry(return_book_window, font=("Arial", 12), date_pattern='y-mm-dd')
    entry_return_date.pack(pady=5)
    
    tk.Button(return_book_window, text="Return Book", font=("Arial", 12), command=submit_return).pack(pady=20)


def add_admin():
    def submit_admin():
        username = entry_username.get()
        password = entry_password.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO admins (username, password) 
                          VALUES (?, ?)''',
                       (username, password))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", f"Admin added with Username: {username}")
        add_admin_window.destroy()

    add_admin_window = tk.Toplevel()
    add_admin_window.title("Add Admin")
    
    labels = ["Username", "Password"]
    entries = []
    
    for label in labels:
        tk.Label(add_admin_window, text=label, font=("Arial", 12)).pack(pady=5)
        entry = tk.Entry(add_admin_window, font=("Arial", 12))
        entry.pack(pady=5)
        entries.append(entry)
    
    entry_username, entry_password = entries
    
    tk.Button(add_admin_window, text="Submit", font=("Arial", 12), command=submit_admin).pack(pady=20)

def fetch_student_details():
    def display_student():
        card_no = entry_card_no.get()
        
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE unique_card_no = ?', (card_no,))
        student = cursor.fetchone()
        
        if student:
            result = f"Name: {student[1]}\nClass: {student[2]}\nRoll No.: {student[3]}\nAdmission No.: {student[4]}"
            messagebox.showinfo("Student Details", result)
        else:
            messagebox.showerror("Error", "Student not found")
        
        conn.close()
    
    fetch_student_details_window = tk.Toplevel()
    fetch_student_details_window.title("Fetch Student Details")
    
    tk.Label(fetch_student_details_window, text="Card No.", font=("Arial", 12)).pack(pady=5)
    entry_card_no = tk.Entry(fetch_student_details_window, font=("Arial", 12))
    entry_card_no.pack(pady=5)
    tk.Button(fetch_student_details_window, text="Fetch Details", font=("Arial", 12), command=display_student).pack(pady=20)

# Main Login Window
login_window = tk.Tk()
login_window.title("Library Management System - Login")

tk.Label(login_window, text="Username", font=("Arial", 12)).pack(pady=5)
entry_username = tk.Entry(login_window, font=("Arial", 12))
entry_username.pack(pady=5)

tk.Label(login_window, text="Password", font=("Arial", 12)).pack(pady=5)
entry_password = tk.Entry(login_window, font=("Arial", 12), show="*")
entry_password.pack(pady=5)

tk.Button(login_window, text="Login", font=("Arial", 12), command=login).pack(pady=20)

login_window.mainloop()
