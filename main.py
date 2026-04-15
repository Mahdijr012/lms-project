
import tkinter as tk
from gui import LibraryGUI
from src.services.member_collection import MemberCollection
from src.services.book_collection import BookCollection
from src.services.loan_service import LoanService
from src.models.book import Book
from src.models.member import Member
import json
import os

# --- Add this right above def main(): ---

DATA_FILE = "library_data.json"

def load_data(book_system, member_system):
    """Loads data from the JSON file into your system on startup."""
    if not os.path.exists(DATA_FILE):
        return # File doesn't exist yet, do nothing

    with open(DATA_FILE, "r") as file:
        try:
            data = json.load(file)
            
            # Load Books
            for b_data in data.get("books", []):
                book = Book(b_data["title"], b_data["author"], b_data["isbn"], b_data["year"])
                book.is_borrowed = b_data.get("is_borrowed", False)
                book_system.add_book(book)
                
            # Load Members
            for m_data in data.get("members", []):
                member = Member(m_data["name"], m_data["member_id"])
                member_system.add_member(member)
                
        except json.JSONDecodeError:
            print("Error reading JSON file. Starting with empty data.")

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

def main():
    # 1. Initialize the root window
    root = tk.Tk()

    # 2. Initialize the Backend Services
    book_system = BookCollection()
    member_system = MemberCollection()
    loan_system = LoanService(book_system, member_system)

    # ---> NEW: Load data from JSON into the systems <---
    load_data(book_system, member_system)

    # 3. Launch the GUI
    app = LibraryGUI(root, book_system, member_system, loan_system)
    
    # 4. Update the GUI tables immediately with the loaded data
    app.refresh_books()
    app.refresh_members()

    # 5. Start the program loop (The app pauses here while the window is open)
    root.mainloop()
    
    # ---> NEW: Save data to JSON when the user closes the window <---
    save_data(book_system, member_system)

if __name__ == "__main__":
    main()