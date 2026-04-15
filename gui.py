import tkinter as tk
from tkinter import ttk, messagebox

from src.models.member import Member
from src.models.book import Book

class LibraryGUI:
    def __init__(self, root, book_system, member_system, loan_system):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("950x650")
        self.root.configure(bg="#f8f9fa") # Light grey background like your photo

        # Connections to backend passed from main.py
        self.book_system = book_system
        self.member_system = member_system
        self.loan_system = loan_system

        # Book entry attributes (initialized in build_books_tab)

        # Header
        header_label = tk.Label(self.root, text="Library Management System", font=("Helvetica", 22, "bold"), fg="#1b3d6d", bg="#f8f9fa")
        header_label.pack(pady=15)

        # Notebook (Tabs)
        style = ttk.Style()
        style.theme_use('default')
        # Style the tabs to look like your photo (grey tabs, white text area)
        style.configure("TNotebook", background="#f8f9fa")
        style.configure("TNotebook.Tab", padding=[20, 5], font=('Helvetica', 10, 'bold'), background="#d3d3d3")
        style.map("TNotebook.Tab", background=[("selected", "white")])
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both', padx=15, pady=(0, 15))

        self.tab_members = tk.Frame(self.notebook, bg="white", bd=1, relief="solid")
        self.tab_books = tk.Frame(self.notebook, bg="white", bd=1, relief="solid")
        self.tab_search = tk.Frame(self.notebook, bg="white", bd=1, relief="solid")
        self.tab_borrow = tk.Frame(self.notebook, bg="white", bd=1, relief="solid")
        self.tab_return = tk.Frame(self.notebook, bg="white", bd=1, relief="solid")
        
        self.notebook.add(self.tab_members, text='Members')
        self.notebook.add(self.tab_books, text='Books')
        self.notebook.add(self.tab_search, text='Search')
        self.notebook.add(self.tab_borrow, text='Borrow Book')
        self.notebook.add(self.tab_return, text='Return Book')

        self.build_members_tab()
        self.build_books_tab()
        self.build_search_tab()
        self.build_borrow_tab()
        self.build_return_tab()

    # ==========================
    # MEMBERS TAB
    # ==========================
    def build_members_tab(self):
        left_frame = tk.Frame(self.tab_members, bd=1, relief="solid", bg="white")
        left_frame.pack(side="left", fill="y", padx=15, pady=15)

        tk.Label(left_frame, text="Manage Members", font=("Helvetica", 14, "bold"), fg="#1b3d6d", bg="white").pack(pady=(20, 20), padx=30)

        tk.Label(left_frame, text="Member Name", font=("Helvetica", 9), bg="white").pack(anchor="w", padx=15)
        self.entry_mem_name = ttk.Entry(left_frame, width=30)
        self.entry_mem_name.pack(padx=15, pady=(2, 15))

        tk.Label(left_frame, text="Member ID", font=("Helvetica", 9), bg="white").pack(anchor="w", padx=15)
        self.entry_mem_id = ttk.Entry(left_frame, width=30)
        self.entry_mem_id.pack(padx=15, pady=(2, 25))

        ttk.Button(left_frame, text="Register Member", command=self.register_member).pack(fill="x", padx=15, pady=8, ipady=4)
        ttk.Button(left_frame, text="Delete Member", command=self.delete_member).pack(fill="x", padx=15, pady=8, ipady=4)
        ttk.Button(left_frame, text="Refresh Members", command=self.refresh_members).pack(fill="x", padx=15, pady=8, ipady=4)

        right_frame = tk.Frame(self.tab_members, bd=1, relief="solid", bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.member_tree = ttk.Treeview(right_frame, columns=("Name", "Member ID"), show="headings")
        self.member_tree.heading("Name", text="Name")
        self.member_tree.heading("Member ID", text="Member ID")
        self.member_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def register_member(self):
        name, mem_id = self.entry_mem_name.get().strip(), self.entry_mem_id.get().strip()
        if not name or not mem_id: return messagebox.showwarning("Error", "Fill all fields.")
        try:
            self.member_system.add_member(Member(name, mem_id))
            self.entry_mem_name.delete(0, tk.END); self.entry_mem_id.delete(0, tk.END)
            self.refresh_members()
            messagebox.showinfo("Success", "Member Registered!")
        except Exception as e: messagebox.showerror("Error", str(e))

    def delete_member(self):
        selected = self.member_tree.selection()
        if not selected: return messagebox.showwarning("Error", "Select a member.")
        try:
            self.member_system.remove_member(self.member_tree.item(selected[0], "values")[1])
            self.refresh_members()
        except Exception as e: messagebox.showerror("Error", str(e))

    def refresh_members(self):
        for item in self.member_tree.get_children(): self.member_tree.delete(item)
        for m in self.member_system.get_all_members(): self.member_tree.insert("", "end", values=(m.name, m.member_id))

    # ==========================
    # BOOKS TAB
    # ==========================
    def build_books_tab(self):
        left_frame = tk.Frame(self.tab_books, bd=1, relief="solid", bg="white")
        left_frame.pack(side="left", fill="y", padx=15, pady=15)

        tk.Label(left_frame, text="Manage Books", font=("Helvetica", 14, "bold"), fg="#1b3d6d", bg="white").pack(pady=(20, 20), padx=30)
        
        # Inputs
        tk.Label(left_frame, text="Title", font=("Helvetica", 9), bg="white").pack(anchor="w", padx=15)
        self.entry_book_title = ttk.Entry(left_frame, width=30)
        self.entry_book_title.pack(padx=15, pady=(2, 10))
        
        tk.Label(left_frame, text="Author", font=("Helvetica", 9), bg="white").pack(anchor="w", padx=15)
        self.entry_book_author = ttk.Entry(left_frame, width=30)
        self.entry_book_author.pack(padx=15, pady=(2, 10))
        
        tk.Label(left_frame, text="ISBN", font=("Helvetica", 9), bg="white").pack(anchor="w", padx=15)
        self.entry_book_isbn = ttk.Entry(left_frame, width=30)
        self.entry_book_isbn.pack(padx=15, pady=(2, 10))
        
        tk.Label(left_frame, text="Year", font=("Helvetica", 9), bg="white").pack(anchor="w", padx=15)
        self.entry_book_year = ttk.Entry(left_frame, width=30)
        self.entry_book_year.pack(padx=15, pady=(2, 25))

        ttk.Button(left_frame, text="Add Book", command=self.add_book).pack(fill="x", padx=15, pady=8, ipady=4)
        ttk.Button(left_frame, text="Delete Book", command=self.delete_book).pack(fill="x", padx=15, pady=5, ipady=4)
        ttk.Button(left_frame, text="Refresh Books", command=self.refresh_books).pack(fill="x", padx=15, pady=5, ipady=4)

        right_frame = tk.Frame(self.tab_books, bd=1, relief="solid", bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.book_tree = ttk.Treeview(right_frame, columns=("Title", "Author", "ISBN", "Status"), show="headings")
        for col in ["Title", "Author", "ISBN", "Status"]: self.book_tree.heading(col, text=col)
        self.book_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_book(self):
        t, a, i, y = self.entry_book_title.get(), self.entry_book_author.get(), self.entry_book_isbn.get(), self.entry_book_year.get()
        if not all([t, a, i, y]): return messagebox.showwarning("Error", "Fill all fields.")
        try:
            self.book_system.add_book(Book(t, a, i, int(y)))
            for attr in ["title", "author", "isbn", "year"]: getattr(self, f"entry_book_{attr}").delete(0, tk.END)
            self.refresh_books()
        except Exception as e: messagebox.showerror("Error", str(e))

    def delete_book(self):
        selected = self.book_tree.selection()
        if not selected: return messagebox.showwarning("Error", "Select a book.")
        try:
            self.book_system.remove_book(self.book_tree.item(selected[0], "values")[2])
            self.refresh_books()
        except Exception as e: messagebox.showerror("Error", str(e))

    def refresh_books(self):
        for item in self.book_tree.get_children(): self.book_tree.delete(item)
        for b in self.book_system.get_all_books():
            self.book_tree.insert("", "end", values=(b.title, b.author, b.isbn, "Borrowed" if b.is_borrowed else "Available"))

    # ==========================
    # SEARCH TAB
    # ==========================
    def build_search_tab(self):
        pass

    # ==========================
    # BORROW / RETURN TABS
    # ==========================
    def build_borrow_tab(self):
        f = tk.Frame(self.tab_borrow, bd=1, relief="solid", bg="white")
        f.place(relx=0.5, rely=0.4, anchor="center")
        tk.Label(f, text="Borrow Book", font=("Helvetica", 14, "bold"), fg="#1b3d6d", bg="white").pack(pady=20, padx=50)
        
        tk.Label(f, text="Member ID", bg="white").pack(anchor="w", padx=30)
        self.b_mem = ttk.Entry(f, width=35); self.b_mem.pack(padx=30, pady=(2, 10))
        tk.Label(f, text="Book ISBN", bg="white").pack(anchor="w", padx=30)
        self.b_isbn = ttk.Entry(f, width=35); self.b_isbn.pack(padx=30, pady=(2, 20))
        
        ttk.Button(f, text="Process Checkout", command=self.borrow_book).pack(fill="x", padx=30, pady=20, ipady=4)

    def build_return_tab(self):
        f = tk.Frame(self.tab_return, bd=1, relief="solid", bg="white")
        f.place(relx=0.5, rely=0.4, anchor="center")
        tk.Label(f, text="Return Book", font=("Helvetica", 14, "bold"), fg="#1b3d6d", bg="white").pack(pady=20, padx=50)
        
        tk.Label(f, text="Book ISBN", bg="white").pack(anchor="w", padx=30)
        self.r_isbn = ttk.Entry(f, width=35); self.r_isbn.pack(padx=30, pady=(2, 20))
        
        ttk.Button(f, text="Process Return", command=self.return_book).pack(fill="x", padx=30, pady=20, ipady=4)

    def borrow_book(self):
        success, msg = self.loan_system.check_out_book(self.b_mem.get(), self.b_isbn.get())
        if success:
            messagebox.showinfo("Success", msg); self.refresh_books()
        else: messagebox.showwarning("Failed", msg)

    def return_book(self):
        success, msg = self.loan_system.check_in_book(self.r_isbn.get())
        if success:
            messagebox.showinfo("Success", msg); self.refresh_books()
        else: messagebox.showwarning("Failed", msg)