import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- BACKEND IMPORTS ---
from src.models.member import Member
from src.services.member_collection import MemberCollection
from src.models.book import Book
from src.services.book_collection import BookCollection
from src.services.loan_service import LoanService

# ==========================================
#        JSON DATA STORAGE FUNCTIONS
# ==========================================
DATA_FILE = "library_data.json"

def load_data(book_system, member_system):
    """Loads data from the JSON file into your system on startup."""
    if not os.path.exists(DATA_FILE):
        return  # File doesn't exist yet, start fresh

    with open(DATA_FILE, "r") as file:
        try:
            data = json.load(file)
            
            # Load Books safely using .get() to prevent KeyErrors
            for b_data in data.get("books", []):
                title = b_data.get("title", "Unknown Title")
                author = b_data.get("author", "Unknown Author")
                isbn = b_data.get("isbn", "Unknown ISBN")
                year = b_data.get("year", 2000) # Defaults to 2000 if year is missing
                
                book = Book(title, author, isbn, int(year))
                book.is_borrowed = b_data.get("is_borrowed", False)
                
                try:
                    book_system.add_book(book)
                except ValueError:
                    pass # Ignore if duplicate
                
            # Load Members safely
            for m_data in data.get("members", []):
                name = m_data.get("name", "Unknown")
                mem_id = m_data.get("member_id", "Unknown")
                
                member = Member(name, mem_id)
                try:
                    member_system.add_member(member)
                except ValueError:
                    pass # Ignore if duplicate
                
        except json.JSONDecodeError:
            print("Error reading JSON file. Starting with empty data.")
        except Exception as e:
            print(f"An error occurred while loading data: {e}")

def save_data(book_system, member_system):
    """Saves all data from your system into the JSON file on exit."""
    data = {
        "books": [],
        "members": []
    }
    
    # Format Books for JSON
    for book in book_system.get_all_books():
        data["books"].append({
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "year": book.year,
            "is_borrowed": book.is_borrowed
        })
        
    # Format Members for JSON
    for member in member_system.get_all_members():
        data["members"].append({
            "name": member.name,
            "member_id": member.member_id
        })
        
    # Write to the file
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# ==========================================
#             GUI CLASS
# ==========================================
class LibraryGUI:
    def __init__(self, root, book_system, member_system, loan_system):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("950x650")
        self.root.configure(bg="#f8f9fa")

        # Connections to backend
        self.book_system = book_system
        self.member_system = member_system
        self.loan_system = loan_system

        # Header
        header_label = tk.Label(self.root, text="Library Management System", font=("Helvetica", 22, "bold"), fg="#1b3d6d", bg="#f8f9fa")
        header_label.pack(pady=15)

        # Notebook (Tabs) setup
        style = ttk.Style()
        style.theme_use('default')
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
        if not name or not mem_id: 
            return messagebox.showwarning("Error", "Fill all fields.")
        try:
            self.member_system.add_member(Member(name, mem_id))
            self.entry_mem_name.delete(0, tk.END)
            self.entry_mem_id.delete(0, tk.END)
            self.refresh_members()
            messagebox.showinfo("Success", "Member Registered!")
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def delete_member(self):
        selected = self.member_tree.selection()
        if not selected: 
            return messagebox.showwarning("Error", "Select a member.")
        try:
            self.member_system.remove_member(self.member_tree.item(selected[0], "values")[1])
            self.refresh_members()
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def refresh_members(self):
        for item in self.member_tree.get_children(): 
            self.member_tree.delete(item)
        for m in self.member_system.get_all_members(): 
            self.member_tree.insert("", "end", values=(m.name, m.member_id))

    # ==========================
    # BOOKS TAB
    # ==========================
    def build_books_tab(self):
        left_frame = tk.Frame(self.tab_books, bd=1, relief="solid", bg="white")
        left_frame.pack(side="left", fill="y", padx=15, pady=15)

        tk.Label(left_frame, text="Manage Books", font=("Helvetica", 14, "bold"), fg="#1b3d6d", bg="white").pack(pady=(20, 20), padx=30)
        
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
        self.entry_book_year.pack(padx=15, pady=(2, 20))

        ttk.Button(left_frame, text="Add Book", command=self.add_book).pack(fill="x", padx=15, pady=5, ipady=4)
        ttk.Button(left_frame, text="Delete Book", command=self.delete_book).pack(fill="x", padx=15, pady=5, ipady=4)
        ttk.Button(left_frame, text="Refresh Books", command=self.refresh_books).pack(fill="x", padx=15, pady=5, ipady=4)

        right_frame = tk.Frame(self.tab_books, bd=1, relief="solid", bg="white")
        right_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.book_tree = ttk.Treeview(right_frame, columns=("Title", "Author", "ISBN", "Year", "Status"), show="headings")
        for col in ["Title", "Author", "ISBN", "Year", "Status"]: 
            self.book_tree.heading(col, text=col)
        self.book_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def add_book(self):
        t = self.entry_book_title.get().strip()
        a = self.entry_book_author.get().strip()
        i = self.entry_book_isbn.get().strip()
        y = self.entry_book_year.get().strip()
        
        if not all([t, a, i, y]): 
            return messagebox.showwarning("Error", "Fill all fields.")
        try:
            self.book_system.add_book(Book(t, a, i, int(y)))
            self.entry_book_title.delete(0, tk.END)
            self.entry_book_author.delete(0, tk.END)
            self.entry_book_isbn.delete(0, tk.END)
            self.entry_book_year.delete(0, tk.END)
            self.refresh_books()
        except ValueError:
            messagebox.showerror("Error", "Year must be a number.")
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def delete_book(self):
        selected = self.book_tree.selection()
        if not selected: 
            return messagebox.showwarning("Error", "Select a book.")
        try:
            self.book_system.remove_book(self.book_tree.item(selected[0], "values")[2])
            self.refresh_books()
        except Exception as e: 
            messagebox.showerror("Error", str(e))

    def refresh_books(self):
        for item in self.book_tree.get_children(): 
            self.book_tree.delete(item)
        for b in self.book_system.get_all_books():
            status = "Borrowed" if b.is_borrowed else "Available"
            self.book_tree.insert("", "end", values=(b.title, b.author, b.isbn, b.year, status))

    # ==========================
    # SEARCH TAB
    # ==========================
    def build_search_tab(self):
        top_frame = tk.Frame(self.tab_search, bg="white")
        top_frame.pack(fill="x", padx=20, pady=20)

        tk.Label(top_frame, text="Search by Title:", font=("Helvetica", 12, "bold"), bg="white").pack(side="left", padx=10)
        self.entry_search = ttk.Entry(top_frame, width=40)
        self.entry_search.pack(side="left", padx=10)
        ttk.Button(top_frame, text="Search", command=self.search_books).pack(side="left", padx=10)

        self.search_tree = ttk.Treeview(self.tab_search, columns=("Title", "Author", "ISBN", "Status"), show="headings")
        for col in ["Title", "Author", "ISBN", "Status"]:
            self.search_tree.heading(col, text=col)
        self.search_tree.pack(fill="both", expand=True, padx=20, pady=10)

    def search_books(self):
        query = self.entry_search.get().strip()
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
            
        results = self.book_system.find_by_title(query)
        for b in results:
            status = "Borrowed" if b.is_borrowed else "Available"
            self.search_tree.insert("", "end", values=(b.title, b.author, b.isbn, status))

    # ==========================
    # BORROW / RETURN TABS
    # ==========================
    def build_borrow_tab(self):
        f = tk.Frame(self.tab_borrow, bd=1, relief="solid", bg="white")
        f.place(relx=0.5, rely=0.4, anchor="center")
        tk.Label(f, text="Borrow Book", font=("Helvetica", 14, "bold"), fg="#1b3d6d", bg="white").pack(pady=20, padx=50)
        
        tk.Label(f, text="Member ID", bg="white").pack(anchor="w", padx=30)
        self.b_mem = ttk.Entry(f, width=35)
        self.b_mem.pack(padx=30, pady=(2, 10))
        
        tk.Label(f, text="Book ISBN", bg="white").pack(anchor="w", padx=30)
        self.b_isbn = ttk.Entry(f, width=35)
        self.b_isbn.pack(padx=30, pady=(2, 20))
        
        ttk.Button(f, text="Process Checkout", command=self.borrow_book).pack(fill="x", padx=30, pady=20, ipady=4)

    def build_return_tab(self):
        f = tk.Frame(self.tab_return, bd=1, relief="solid", bg="white")
        f.place(relx=0.5, rely=0.4, anchor="center")
        tk.Label(f, text="Return Book", font=("Helvetica", 14, "bold"), fg="#1b3d6d", bg="white").pack(pady=20, padx=50)
        
        tk.Label(f, text="Book ISBN", bg="white").pack(anchor="w", padx=30)
        self.r_isbn = ttk.Entry(f, width=35)
        self.r_isbn.pack(padx=30, pady=(2, 20))
        
        ttk.Button(f, text="Process Return", command=self.return_book).pack(fill="x", padx=30, pady=20, ipady=4)

    def borrow_book(self):
        success, msg = self.loan_system.check_out_book(self.b_mem.get(), self.b_isbn.get())
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_books()
        else: 
            messagebox.showwarning("Failed", msg)

    def return_book(self):
        success, msg = self.loan_system.check_in_book(self.r_isbn.get())
        if success:
            messagebox.showinfo("Success", msg)
            self.refresh_books()
        else: 
            messagebox.showwarning("Failed", msg)

# ==========================================
#             ENTRY POINT
# ==========================================
def main():
    root = tk.Tk()

    # Initialize the Backend Services
    book_system = BookCollection()
    member_system = MemberCollection()
    loan_system = LoanService(book_system, member_system)

    # Load Data from JSON
    load_data(book_system, member_system)

    # Launch GUI
    app = LibraryGUI(root, book_system, member_system, loan_system)
    
    # Refresh tables to show loaded data
    app.refresh_books()
    app.refresh_members()

    # Start Program
    root.mainloop()
    
    # Save Data to JSON when window is closed
    save_data(book_system, member_system)

if __name__ == "__main__":
    main()