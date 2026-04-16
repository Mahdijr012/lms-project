import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from src.models.book import Book
from src.models.member import Member

class LibraryDashboard:
    def __init__(self, root, book_system, member_system, loan_system):
        self.root = root
        self.root.title("Library Management System - Admin Dashboard")
        self.root.geometry("1100x700")
        self.root.configure(bg="#ecf0f5")

        self.book_system = book_system
        self.member_system = member_system
        self.loan_system = loan_system

        # --- LAYOUT FRAMES ---
        self.sidebar = tk.Frame(self.root, bg="#2c3e50", width=220)
        self.sidebar.pack(side="left", fill="y")
        
        self.main_content = tk.Frame(self.root, bg="#ecf0f5")
        self.main_content.pack(side="right", fill="both", expand=True)

        self.build_sidebar()
        self.show_home() # Default screen

    # ==========================================
    #             SIDEBAR MENU
    # ==========================================
    def build_sidebar(self):
        tk.Label(self.sidebar, text="LMS Admin", font=("Helvetica", 18, "bold"), fg="white", bg="#2c3e50").pack(pady=30)

        buttons = [
            ("🏠 Dashboard Overview", self.show_home),
            ("📚 Manage Books", self.show_books),
            ("👥 Manage Members", self.show_members),
            ("🔄 Checkout / Return", self.show_loans),
            ("📊 View Reports", self.show_reports)
        ]

        for text, command in buttons:
            btn = tk.Button(self.sidebar, text=text, font=("Helvetica", 12), fg="white", bg="#34495e", 
                            bd=0, activebackground="#1abc9c", anchor="w", padx=20, command=command)
            btn.pack(fill="x", pady=2, ipady=10)

    def clear_main(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    # ==========================================
    #             1. HOME DASHBOARD
    # ==========================================
    def show_home(self):
        self.clear_main()
        tk.Label(self.main_content, text="System Overview", font=("Helvetica", 24, "bold"), bg="#ecf0f5", fg="#2c3e50").pack(pady=30, anchor="w", padx=40)

        cards_frame = tk.Frame(self.main_content, bg="#ecf0f5")
        cards_frame.pack(fill="x", padx=40)

        def make_card(parent, title, value, color):
            f = tk.Frame(parent, bg=color, width=220, height=130)
            f.pack_propagate(False)
            f.pack(side="left", padx=15, expand=True, fill="both")
            tk.Label(f, text=title, font=("Helvetica", 14), fg="white", bg=color).pack(pady=(25, 5))
            tk.Label(f, text=str(value), font=("Helvetica", 28, "bold"), fg="white", bg=color).pack()

        make_card(cards_frame, "Total Book Titles", len(self.book_system.get_all_books()), "#3498db")
        make_card(cards_frame, "Registered Members", len(self.member_system.get_all_members()), "#2ecc71")
        make_card(cards_frame, "Active Loans", len(self.loan_system.active_loans), "#e74c3c")

    # ==========================================
    #             2. BOOK MANAGEMENT
    # ==========================================
    def show_books(self):
        self.clear_main()
        tk.Label(self.main_content, text="Book Management", font=("Helvetica", 24, "bold"), bg="#ecf0f5", fg="#2c3e50").pack(pady=20, anchor="w", padx=40)

        # Input Frame
        controls = tk.Frame(self.main_content, bg="white", bd=1, relief="solid", padx=20, pady=20)
        controls.pack(fill="x", padx=40, pady=10)

        tk.Label(controls, text="Title:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        title_entry = ttk.Entry(controls, width=25); title_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(controls, text="Author:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        author_entry = ttk.Entry(controls, width=25); author_entry.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(controls, text="ISBN:", bg="white").grid(row=1, column=0, padx=5, pady=5)
        isbn_entry = ttk.Entry(controls, width=25); isbn_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(controls, text="Year:", bg="white").grid(row=1, column=2, padx=5, pady=5)
        year_entry = ttk.Entry(controls, width=10); year_entry.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        tk.Label(controls, text="Copies:", bg="white").grid(row=1, column=4, padx=5, pady=5)
        copies_entry = ttk.Entry(controls, width=10); copies_entry.grid(row=1, column=5, padx=5, pady=5)

        # Table Frame
        table_frame = tk.Frame(self.main_content, bg="white", bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, padx=40, pady=10)

        cols = ("Title", "Author", "ISBN", "Year", "Availability")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        def refresh():
            for item in tree.get_children(): tree.delete(item)
            for b in self.book_system.get_all_books():
                tree.insert("", "end", values=(b.title, b.author, b.isbn, b.year, f"{b.available_copies} / {b.total_copies}"))

        def add():
            try:
                b = Book(title_entry.get(), author_entry.get(), isbn_entry.get(), int(year_entry.get()), int(copies_entry.get() or 1))
                self.book_system.add_book(b)
                refresh(); messagebox.showinfo("Success", "Book Added")
            except Exception as e: messagebox.showerror("Error", str(e))

        def delete():
            sel = tree.selection()
            if not sel: return messagebox.showwarning("Error", "Select a book")
            try:
                self.book_system.remove_book(tree.item(sel[0], "values")[2])
                refresh()
            except Exception as e: messagebox.showerror("Error", str(e))

        ttk.Button(controls, text="Add Book", command=add).grid(row=0, column=6, padx=10, ipady=3)
        ttk.Button(controls, text="Delete Book", command=delete).grid(row=1, column=6, padx=10, ipady=3)
        refresh()

    # ==========================================
    #             3. MEMBER MANAGEMENT
    # ==========================================
    def show_members(self):
        self.clear_main()
        tk.Label(self.main_content, text="Member Management", font=("Helvetica", 24, "bold"), bg="#ecf0f5", fg="#2c3e50").pack(pady=20, anchor="w", padx=40)

        controls = tk.Frame(self.main_content, bg="white", bd=1, relief="solid", padx=20, pady=20)
        controls.pack(fill="x", padx=40, pady=10)

        tk.Label(controls, text="Name:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(controls, width=30); name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(controls, text="Member ID:", bg="white").grid(row=0, column=2, padx=5, pady=5)
        id_entry = ttk.Entry(controls, width=30); id_entry.grid(row=0, column=3, padx=5, pady=5)

        table_frame = tk.Frame(self.main_content, bg="white", bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, padx=40, pady=10)

        cols = ("Name", "Member ID", "Books Borrowed", "Fines Owed")
        tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols: tree.heading(c, text=c)
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        def refresh():
            for item in tree.get_children(): tree.delete(item)
            for m in self.member_system.get_all_members():
                tree.insert("", "end", values=(m.name, m.member_id, len(m.get_borrowed_books()), f"${m.fines_owed:.2f}"))

        def add():
            try:
                self.member_system.add_member(Member(name_entry.get(), id_entry.get()))
                refresh(); messagebox.showinfo("Success", "Member Registered")
            except Exception as e: messagebox.showerror("Error", str(e))

        def delete():
            sel = tree.selection()
            if not sel: return messagebox.showwarning("Error", "Select a member")
            try:
                self.member_system.remove_member(tree.item(sel[0], "values")[1])
                refresh()
            except Exception as e: messagebox.showerror("Error", str(e))

        def pay_fine():
            sel = tree.selection()
            if not sel: return messagebox.showwarning("Error", "Select a member")
            mem = self.member_system.find_member_by_id(tree.item(sel[0], "values")[1])
            if not mem:
                return messagebox.showerror("Error", "Selected member not found.")
            mem.fines_owed = 0.0 # Simplistic pay-off
            refresh(); messagebox.showinfo("Success", "Fines cleared.")
    
        ttk.Button(controls, text="Register", command=add).grid(row=0, column=4, padx=10)
        ttk.Button(controls, text="Delete", command=delete).grid(row=0, column=5, padx=10)
        ttk.Button(controls, text="Clear Fines", command=pay_fine).grid(row=0, column=6, padx=10)
        refresh()

    # ==========================================
    #             5. REPORTS
    # ==========================================
    def show_reports(self):
        self.clear_main()
        tk.Label(self.main_content, text="Reports", font=("Helvetica", 24, "bold"), bg="#ecf0f5", fg="#2c3e50").pack(pady=20, anchor="w", padx=40)

    # ==========================================
    #             4. LOANS (CHECKOUT/RETURN)
    # ==========================================
    def show_loans(self):
        self.clear_main()
        tk.Label(self.main_content, text="Loan Operations", font=("Helvetica", 24, "bold"), bg="#ecf0f5", fg="#2c3e50").pack(pady=20, anchor="w", padx=40)

        f = tk.Frame(self.main_content, bg="white", bd=1, relief="solid", padx=40, pady=40)
        f.pack(fill="x", padx=40, pady=10)

        # Checkout / Return section
        tk.Label(f, text="Check Out / Return Book", font=("Helvetica", 16, "bold"), fg="#2980b9", bg="white").grid(row=0, column=0, columnspan=6, pady=(0,20), sticky="w")

        tk.Label(f, text="Member ID:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        member_id_entry = ttk.Entry(f, width=25)
        member_id_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(f, text="ISBN:", bg="white").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        isbn_entry = ttk.Entry(f, width=25)
        isbn_entry.grid(row=1, column=3, padx=5, pady=5)

        def refresh_loans():
            for item in loan_tree.get_children():
                loan_tree.delete(item)
            for loan in self.loan_system.active_loans:
                loan_tree.insert(
                    "",
                    "end",
                    values=(
                        loan.member.name,
                        loan.member.member_id,
                        loan.book.title,
                        loan.book.isbn,
                        loan.due_date.strftime("%Y-%m-%d"),
                    ),
                )

        def checkout():
            member_id = member_id_entry.get().strip()
            isbn = isbn_entry.get().strip()
            if not member_id or not isbn:
                return messagebox.showwarning("Error", "Member ID and ISBN are required.")

            success, msg = self.loan_system.check_out_book(member_id, isbn)
            if success:
                refresh_loans()
                member_id_entry.delete(0, "end")
                isbn_entry.delete(0, "end")
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)

        def return_book():
            isbn = isbn_entry.get().strip()
            if not isbn:
                sel = loan_tree.selection()
                if sel:
                    isbn = loan_tree.item(sel[0], "values")[3]

            if not isbn:
                return messagebox.showwarning("Error", "Enter or select an ISBN to return.")

            success, msg = self.loan_system.check_in_book(isbn)
            if success:
                refresh_loans()
                isbn_entry.delete(0, "end")
                messagebox.showinfo("Success", msg)
            else:
                messagebox.showerror("Error", msg)

        ttk.Button(f, text="Check Out", command=checkout).grid(row=1, column=4, padx=10, ipady=3)
        ttk.Button(f, text="Return Book", command=return_book).grid(row=1, column=5, padx=10, ipady=3)

        table_frame = tk.Frame(self.main_content, bg="white", bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, padx=40, pady=10)

        cols = ("Member", "Member ID", "Title", "ISBN", "Due Date")
        loan_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            loan_tree.heading(c, text=c)
        loan_tree.pack(fill="both", expand=True, padx=10, pady=10)

        refresh_loans()
        