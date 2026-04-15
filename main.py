
# main.py
import tkinter as tk
from tkinter import ttk, messagebox

# --- Backend Imports ---
# We import all our backend logic and models. The GUI will use them.
from src.models.book import Book
from src.models.member import Member
from src.services.book_collection import BookCollection
from src.services.member_collection import MemberCollection
from src.services.loan_service import LoanService

class LibraryApp(tk.Tk):
    """
    The main GUI application window for the Library Management System.
    This class is responsible for the user interface (the "view").
    It interacts with the backend services to perform actions.
    """
    def __init__(self, book_collection, member_collection, loan_service):
        super().__init__()
        
        # Store references to the backend services
        self.book_collection = book_collection
        self.member_collection = member_collection
        self.loan_service = loan_service

        # --- Window Configuration ---
        self.title("Library Management System")
        self.geometry("700x500")

        # --- Create a Tabbed Interface ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")

        # Create frames for each tab
        self.book_tab = ttk.Frame(self.notebook)
        self.member_tab = ttk.Frame(self.notebook)
        self.loan_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.book_tab, text="Book Management")
        self.notebook.add(self.member_tab, text="Member Management")
        self.notebook.add(self.loan_tab, text="Loan Management")

        # Populate each tab with widgets
        self._create_book_tab_widgets()
        self._create_member_tab_widgets()
        self._create_loan_tab_widgets()

        # Refresh lists on startup
        self._refresh_book_list()
        self._refresh_member_list()

    # --- Widget Creation for Book Tab ---
    def _create_book_tab_widgets(self):
        # Frame for adding a new book
        add_frame = ttk.LabelFrame(self.book_tab, text="Add New Book")
        add_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(add_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.book_title_entry = ttk.Entry(add_frame)
        self.book_title_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_frame, text="Author:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.book_author_entry = ttk.Entry(add_frame)
        self.book_author_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_frame, text="ISBN:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.book_isbn_entry = ttk.Entry(add_frame)
        self.book_isbn_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        add_button = ttk.Button(add_frame, text="Add Book", command=self._add_book)
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame for displaying the list of books
        list_frame = ttk.LabelFrame(self.book_tab, text="Library Catalog")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.book_listbox = tk.Listbox(list_frame)
        self.book_listbox.pack(fill="both", expand=True, side="left")
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.book_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.book_listbox.config(yscrollcommand=scrollbar.set)

    # --- Widget Creation for Member Tab ---
    def _create_member_tab_widgets(self):
        add_frame = ttk.LabelFrame(self.member_tab, text="Add New Member")
        add_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.member_name_entry = ttk.Entry(add_frame)
        self.member_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_frame, text="Member ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.member_id_entry = ttk.Entry(add_frame)
        self.member_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        add_button = ttk.Button(add_frame, text="Add Member", command=self._add_member)
        add_button.grid(row=2, column=0, columnspan=2, pady=10)

        list_frame = ttk.LabelFrame(self.member_tab, text="Registered Members")
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.member_listbox = tk.Listbox(list_frame)
        self.member_listbox.pack(fill="both", expand=True)

    # --- Widget Creation for Loan Tab ---
    def _create_loan_tab_widgets(self):
        checkout_frame = ttk.LabelFrame(self.loan_tab, text="Check Out a Book")
        checkout_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(checkout_frame, text="Member ID:").grid(row=0, column=0, padx=5, pady=5)
        self.checkout_member_id_entry = ttk.Entry(checkout_frame)
        self.checkout_member_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(checkout_frame, text="Book ISBN:").grid(row=1, column=0, padx=5, pady=5)
        self.checkout_book_isbn_entry = ttk.Entry(checkout_frame)
        self.checkout_book_isbn_entry.grid(row=1, column=1, padx=5, pady=5)

        checkout_button = ttk.Button(checkout_frame, text="Check Out", command=self._check_out)
        checkout_button.grid(row=2, column=0, columnspan=2, pady=10)

        checkin_frame = ttk.LabelFrame(self.loan_tab, text="Check In a Book")
        checkin_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(checkin_frame, text="Book ISBN:").grid(row=0, column=0, padx=5, pady=5)
        self.checkin_book_isbn_entry = ttk.Entry(checkin_frame)
        self.checkin_book_isbn_entry.grid(row=0, column=1, padx=5, pady=5)

        checkin_button = ttk.Button(checkin_frame, text="Check In", command=self._check_in)
        checkin_button.grid(row=1, column=0, columnspan=2, pady=10)

    # --- Event Handlers (Connect GUI to Backend) ---

    def _add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        isbn = self.book_isbn_entry.get()
        if not all([title, author, isbn]):
            messagebox.showerror("Error", "All fields are required.")
            return
        
        success, message = self.book_collection.add_book(Book(title, author, isbn))
        
        if success:
            messagebox.showinfo("Success", message)
            self.book_title_entry.delete(0, tk.END)
            self.book_author_entry.delete(0, tk.END)
            self.book_isbn_entry.delete(0, tk.END)
            self._refresh_book_list()
        else:
            messagebox.showerror("Error", message)

    def _add_member(self):
        name = self.member_name_entry.get()
        member_id = self.member_id_entry.get()
        if not all([name, member_id]):
            messagebox.showerror("Error", "All fields are required.")
            return

        success, message = self.member_collection.add_member(Member(name, member_id))

        if success:
            messagebox.showinfo("Success", message)
            self.member_name_entry.delete(0, tk.END)
            self.member_id_entry.delete(0, tk.END)
            self._refresh_member_list()
        else:
            messagebox.showerror("Error", message)

    def _check_out(self):
        member_id = self.checkout_member_id_entry.get()
        isbn = self.checkout_book_isbn_entry.get()
        if not all([member_id, isbn]):
            messagebox.showerror("Error", "Member ID and ISBN are required.")
            return
        
        success, message = self.loan_service.check_out_book(member_id, isbn)

        if success:
            messagebox.showinfo("Success", message)
            self._refresh_book_list() # Update book status display
        else:
            messagebox.showerror("Error", message)

    def _check_in(self):
        isbn = self.checkin_book_isbn_entry.get()
        if not isbn:
            messagebox.showerror("Error", "ISBN is required.")
            return

        success, message = self.loan_service.check_in_book(isbn)

        if success:
            messagebox.showinfo("Success", message)
            self._refresh_book_list() # Update book status display
        else:
            messagebox.showerror("Error", message)

    # --- Helper methods to update the display ---
    
    def _refresh_book_list(self):
        self.book_listbox.delete(0, tk.END) # Clear the list
        all_books = self.book_collection.get_all_books()
        for book in all_books:
            self.book_listbox.insert(tk.END, str(book))

    def _refresh_member_list(self):
        self.member_listbox.delete(0, tk.END) # Clear the list
        all_members = self.member_collection.get_all_members()
        for member in all_members:
            self.member_listbox.insert(tk.END, str(member))

# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Initialize the backend services (the "engine")
    book_collection = BookCollection()
    member_collection = MemberCollection()
    loan_service = LoanService(book_collection, member_collection)

    # 2. Pre-populate with some data for demonstration
    book_collection.add_book(Book("The Hobbit", "J.R.R. Tolkien", "111"))
    book_collection.add_book(Book("1984", "George Orwell", "222"))
    book_collection.add_book(Book("To Kill a Mockingbird", "Harper Lee", "333"))
    member_collection.add_member(Member("Alice", "A001"))
    member_collection.add_member(Member("Bob", "B002"))

    # 3. Create an instance of the GUI application
    app = LibraryApp(book_collection, member_collection, loan_service)

    # 4. Start the GUI event loop
    app.mainloop()
