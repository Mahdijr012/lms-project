# main.py
import tkinter as tk
from tkinter import ttk, messagebox

# --- Backend Imports ---
from src.models.book import Book
from src.models.member import Member
from src.services.book_collection import BookCollection
from src.services.member_collection import MemberCollection
# You would also import LoanService here when you build it

# --- Constants ---
DATA_FILE = 'library_data.json'

class LibraryApp(tk.Tk):
    def __init__(self, book_collection, member_collection):
        super().__init__()
        self.book_collection = book_collection
        self.member_collection = member_collection
        
        self.title("Library Management System")
        self.geometry("800x600")
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

        self.create_members_tab()
        # Add other tabs here...

    def create_members_tab(self):
        members_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(members_frame, text='Members')

        left_panel = ttk.Frame(members_frame)
        left_panel.pack(side='left', fill='y', padx=(0, 10))

        manage_label = ttk.Label(left_panel, text="Manage Members", font=('Helvetica', 12, 'bold'))
        manage_label.pack(pady=10, padx=10, anchor='w')

        ttk.Label(left_panel, text="Member Name").pack(padx=10, anchor='w')
        self.member_name_entry = ttk.Entry(left_panel, width=30)
        self.member_name_entry.pack(padx=10, pady=(0, 10))

        ttk.Label(left_panel, text="Member ID").pack(padx=10, anchor='w')
        self.member_id_entry = ttk.Entry(left_panel, width=30)
        self.member_id_entry.pack(padx=10, pady=(0, 20))

        ttk.Button(left_panel, text="Register Member", command=self._on_register_member).pack(fill='x', padx=10, pady=5)
        ttk.Button(left_panel, text="Delete Member", command=self._on_delete_member).pack(fill='x', padx=10, pady=5)
        ttk.Button(left_panel, text="Refresh Members", command=self.populate_members_list).pack(fill='x', padx=10, pady=5)

        right_panel = ttk.Frame(members_frame, relief="groove", borderwidth=2)
        right_panel.pack(side='right', expand=True, fill='both')

        columns = ('name', 'member_id')
        self.members_tree = ttk.Treeview(right_panel, columns=columns, show='headings')
        self.members_tree.heading('name', text='Name')
        self.members_tree.heading('member_id', text='Member ID')
        self.members_tree.pack(expand=True, fill='both')
        self.populate_members_list()

    def _on_register_member(self):
        name = self.member_name_entry.get()
        member_id = self.member_id_entry.get()
        if not name or not member_id:
            messagebox.showerror("Error", "All fields are required.")
            return

        success, message = self.member_collection.add_member(Member(name, member_id))
        if success:
            messagebox.showinfo("Success", message)
            self.member_name_entry.delete(0, tk.END)
            self.member_id_entry.delete(0, tk.END)
            self.populate_members_list()
        else:
            messagebox.showerror("Error", message)

    def _on_delete_member(self):
        selected_item = self.members_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a member to delete.")
            return

        member_id = self.members_tree.item(selected_item[0], 'values')[1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete member ID '{member_id}'?"):
            success, message = self.member_collection.delete_member(member_id)
            if success:
                messagebox.showinfo("Success", message)
                self.populate_members_list()
            else:
                messagebox.showerror("Error", message)

    def populate_members_list(self):
        for i in self.members_tree.get_children():
            self.members_tree.delete(i)
        for member in self.member_collection.get_all_members():
            self.members_tree.insert('', tk.END, values=(member.name, member.member_id))

    def on_closing(self):
        """Handle the window closing event to save data."""
        if messagebox.askokcancel("Quit", "Do you want to save changes and quit?"):
            self.book_collection.save_data(DATA_FILE)
            self.member_collection.save_data(DATA_FILE)
            self.destroy()

# --- Main Execution Block ---
if __name__ == "__main__":
    # 1. Initialize backend services
    book_collection = BookCollection()
    member_collection = MemberCollection()

    # 2. Load data from the JSON file into the services
    book_collection.load_data(DATA_FILE)
    member_collection.load_data(DATA_FILE)

    # 3. Create and run the GUI, passing the services to it
    app = LibraryApp(book_collection, member_collection)
    app.mainloop()