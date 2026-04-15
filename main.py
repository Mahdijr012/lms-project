# main.py
import tkinter as tk
from tkinter import ttk, messagebox

# --- Backend Imports ---
from src.models.book import Book
from src.models.member import Member
from src.services.book_collection import BookCollection
from src.services.member_collection import MemberCollection
from src.services.loan_service import LoanService
from src.utils.constants import DATA_FILE

class LibraryApp(tk.Tk):
    def __init__(self, book_collection, member_collection, loan_service):
        super().__init__()
        self.book_collection = book_collection
        self.member_collection = member_collection
        self.loan_service = loan_service
        
        self.title("Library Management System")
        self.geometry("850x600")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # --- Style Configuration ---
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=('Helvetica', 10, 'bold'), padding=[10, 5])
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=('Helvetica', 10))
        style.configure("TButton", font=('Helvetica', 10), padding=6)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))

        # --- Main Title ---
        title_label = tk.Label(self, text="Library Management System", font=('Helvetica', 18, 'bold'), bg="#e0e8f0", fg="#2c3e50", pady=10)
        title_label.pack(fill='x')

        # --- Notebook for Tabs ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # --- Create All Tabs ---
        self.create_members_tab()
        self.create_books_tab()
        # self.create_search_tab() # Placeholder for search
        self.create_borrow_tab()
        self.create_return_tab()
        
        # Initial data population
        self.populate_books_list()
        self.populate_members_list()

    # ===================================================================
    # MEMBERS TAB
    # ===================================================================
    def create_members_tab(self):
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text='Members')

        left_panel = ttk.Frame(frame, relief="groove", borderwidth=2, padding=10)
        left_panel.pack(side='left', fill='y', padx=(0, 10))

        ttk.Label(left_panel, text="Manage Members", font=('Helvetica', 12, 'bold')).pack(pady=10, anchor='w')
        ttk.Label(left_panel, text="Member Name").pack(anchor='w')
        self.member_name_entry = ttk.Entry(left_panel, width=30)
        self.member_name_entry.pack(pady=(0, 10))
        ttk.Label(left_panel, text="Member ID").pack(anchor='w')
        self.member_id_entry = ttk.Entry(left_panel, width=30)
        self.member_id_entry.pack(pady=(0, 20))
        ttk.Button(left_panel, text="Register Member", command=self._on_register_member).pack(fill='x', pady=5)
        ttk.Button(left_panel, text="Delete Member", command=self._on_delete_member).pack(fill='x', pady=5)

        right_panel = ttk.Frame(frame)
        right_panel.pack(side='right', expand=True, fill='both')
        columns = ('name', 'member_id')
        self.members_tree = ttk.Treeview(right_panel, columns=columns, show='headings')
        self.members_tree.heading('name', text='Name')
        self.members_tree.heading('member_id', text='Member ID')
        self.members_tree.pack(expand=True, fill='both')

    # ===================================================================
    # BOOKS TAB
    # ===================================================================
    def create_books_tab(self):
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text='Books')

        left_panel = ttk.Frame(frame, relief="groove", borderwidth=2, padding=10)
        left_panel.pack(side='left', fill='y', padx=(0, 10))

        ttk.Label(left_panel, text="Manage Books", font=('Helvetica', 12, 'bold')).pack(pady=10, anchor='w')
        ttk.Label(left_panel, text="Title").pack(anchor='w')
        self.book_title_entry = ttk.Entry(left_panel, width=30)
        self.book_title_entry.pack(pady=(0, 10))
        ttk.Label(left_panel, text="Author").pack(anchor='w')
        self.book_author_entry = ttk.Entry(left_panel, width=30)
        self.book_author_entry.pack(pady=(0, 10))
        ttk.Label(left_panel, text="ISBN").pack(anchor='w')
        self.book_isbn_entry = ttk.Entry(left_panel, width=30)
        self.book_isbn_entry.pack(pady=(0, 20))
        ttk.Button(left_panel, text="Add Book", command=self._on_add_book).pack(fill='x', pady=5)
        ttk.Button(left_panel, text="Delete Book", command=self._on_delete_book).pack(fill='x', pady=5)

        right_panel = ttk.Frame(frame)
        right_panel.pack(side='right', expand=True, fill='both')
        columns = ('title', 'author', 'isbn', 'status')
        self.books_tree = ttk.Treeview(right_panel, columns=columns, show='headings')
        self.books_tree.heading('title', text='Title')
        self.books_tree.heading('author', text='Author')
        self.books_tree.heading('isbn', text='ISBN')
        self.books_tree.heading('status', text='Status')
        self.books_tree.column('status', width=100, anchor='center')
        self.books_tree.pack(expand=True, fill='both')

    # ===================================================================
    # BORROW TAB
    # ===================================================================
    def create_borrow_tab(self):
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text='Borrow Book')

        ttk.Label(frame, text="Borrow a Book", font=('Helvetica', 14, 'bold')).pack(pady=20)
        ttk.Label(frame, text="Member ID:").pack(pady=5)
        self.borrow_member_id_entry = ttk.Entry(frame, width=40)
        self.borrow_member_id_entry.pack(pady=5)
        ttk.Label(frame, text="Book ISBN:").pack(pady=5)
        self.borrow_book_isbn_entry = ttk.Entry(frame, width=40)
        self.borrow_book_isbn_entry.pack(pady=5)
        ttk.Button(frame, text="Confirm Borrow", command=self._on_borrow_book).pack(pady=20)

    # ===================================================================
    # RETURN TAB
    # ===================================================================
    def create_return_tab(self):
        frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(frame, text='Return Book')

        ttk.Label(frame, text="Return a Book", font=('Helvetica', 14, 'bold')).pack(pady=20)
        ttk.Label(frame, text="Book ISBN:").pack(pady=5)
        self.return_book_isbn_entry = ttk.Entry(frame, width=40)
        self.return_book_isbn_entry.pack(pady=5)
        ttk.Button(frame, text="Confirm Return", command=self._on_return_book).pack(pady=20)

    # ===================================================================
    # EVENT HANDLERS & LOGIC
    # ===================================================================
    def _on_register_member(self):
        name = self.member_name_entry.get()
        member_id = self.member_id_entry.get()
        if not name or not member_id: messagebox.showerror("Error", "All fields are required."); return
        success, message = self.member_collection.add_member(Member(name, member_id))
        if success: messagebox.showinfo("Success", message); self.populate_members_list()
        else: messagebox.showerror("Error", message)

    def _on_delete_member(self):
        selected_item = self.members_tree.selection()
        if not selected_item: messagebox.showwarning("Warning", "Please select a member."); return
        member_id = self.members_tree.item(selected_item[0], 'values')[1]
        if messagebox.askyesno("Confirm", f"Delete member {member_id}?"):
            success, message = self.member_collection.delete_member(member_id)
            if success: messagebox.showinfo("Success", message); self.populate_members_list()
            else: messagebox.showerror("Error", message)

    def _on_add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        isbn = self.book_isbn_entry.get()
        if not all([title, author, isbn]): messagebox.showerror("Error", "All fields are required."); return
        success, message = self.book_collection.add_book(Book(title, author, isbn))
        if success: messagebox.showinfo("Success", message); self.populate_books_list()
        else: messagebox.showerror("Error", message)

    def _on_delete_book(self):
        selected_item = self.books_tree.selection()
        if not selected_item: messagebox.showwarning("Warning", "Please select a book."); return
        isbn = self.books_tree.item(selected_item[0], 'values')[2]
        if messagebox.askyesno("Confirm", f"Delete book with ISBN {isbn}?"):
            success, message = self.book_collection.delete_book(isbn)
            if success: messagebox.showinfo("Success", message); self.populate_books_list()
            else: messagebox.showerror("Error", message)

    def _on_borrow_book(self):
        member_id = self.borrow_member_id_entry.get()
        isbn = self.borrow_book_isbn_entry.get()
        if not all([member_id, isbn]): messagebox.showerror("Error", "All fields are required."); return
        success, message = self.loan_service.check_out_book(member_id, isbn)
        if success: messagebox.showinfo("Success", message); self.populate_books_list()
        else: messagebox.showerror("Error", message)

    def _on_return_book(self):
        isbn = self.return_book_isbn_entry.get()
        if not isbn: messagebox.showerror("Error", "ISBN is required."); return
        success, message = self.loan_service.check_in_book(isbn)
        if success: messagebox.showinfo("Success", message); self.populate_books_list()
        else: messagebox.showerror("Error", message)

    def populate_members_list(self):
        for i in self.members_tree.get_children(): self.members_tree.delete(i)
        for member in self.member_collection.get_all_members():
            self.members_tree.insert('', tk.END, values=(member.name, member.member_id))

    def populate_books_list(self):
        for i in self.books_tree.get_children(): self.books_tree.delete(i)
        for book in self.book_collection.get_all_books():
            status = "Borrowed" if book.is_borrowed else "Available"
            self.books_tree.insert('', tk.END, values=(book.title, book.author, book.isbn, status))

    def on_closing(self):
        """Handle the window closing event to save all data."""
        if messagebox.askokcancel("Quit", "Do you want to save all changes and quit?"):
            self.book_collection.save_data(DATA_FILE)
            self.member_collection.save_data(DATA_FILE)
            self.loan_service.save_data(DATA_FILE)
            self.destroy()

# --- Main Execution Block ---
if __name__ == "__main__":
    book_collection = BookCollection()
    member_collection = MemberCollection()
    loan_service = LoanService(book_collection, member_collection)

    book_collection.load_data(DATA_FILE)
    member_collection.load_data(DATA_FILE)
    loan_service.load_data(DATA_FILE)
    
    # Pre-populate with data only if the collections are empty
    if not book_collection.get_all_books():
        book_collection.add_book(Book("The Hobbit", "J.R.R. Tolkien", "111"))
        book_collection.add_book(Book("1984", "George Orwell", "222"))
    if not member_collection.get_all_members():
        member_collection.add_member(Member("Alice", "A001"))

    app = LibraryApp(book_collection, member_collection, loan_service)
    app.mainloop()