# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.models.book import Book
from src.models.member import Member

class LibraryApp(tk.Tk):
    def __init__(self, services):
        super().__init__()
        self.book_service = services['books']
        self.member_service = services['members']
        self.loan_service = services['loans']
        
        self.title("Library Management System")
        self.geometry("900x600")

        # Styles and Main Title (same as before)
        style = ttk.Style(self)
        style.theme_use("clam")
        # ... (all your style configurations)
        title_label = tk.Label(self, text="Library Management System", font=('Helvetica', 18, 'bold'), bg="#e0e8f0", fg="#2c3e50", pady=10)
        title_label.pack(fill='x')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create all tabs
        self.create_members_tab()
        self.create_books_tab()
        self.create_borrow_tab()
        self.create_return_tab()
        
        self.refresh_all_lists()

    def refresh_all_lists(self):
        self.populate_members_list()
        self.populate_books_list()

    def create_members_tab(self):
        # This function creates the UI for the Members tab
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text='Members')
        # ... (Code for members tab widgets from previous response)
        # Use self.member_service instead of self.member_collection
        # Example: ttk.Button(..., command=self._on_register_member)
        self.member_name_entry = ttk.Entry(frame)
        self.member_id_entry = ttk.Entry(frame)

    def create_books_tab(self):
        # This function creates the UI for the Books tab
        frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame, text='Books')
        # ... (Similar UI structure as members tab for adding/deleting books)

    def create_borrow_tab(self):
        # ... (UI for borrow tab)
        pass

    def create_return_tab(self):
        # ... (UI for return tab)
        pass

    def populate_members_list(self):
        # Populate members list in the UI
        pass

    def populate_books_list(self):
        # Populate books list in the UI
        pass

    # --- All _on_... and populate_... methods go here ---
    # Make sure they call self.book_service, self.member_service, etc.
    # For example:
    def _on_register_member(self):
        name = self.member_name_entry.get()
        member_id = self.member_id_entry.get()
        # ... validation ...
        success, message = self.member_service.add_member(Member(name, member_id))
        # ... handle success/error and refresh list ...

    # And so on for all other event handlers...