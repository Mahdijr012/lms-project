
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
                # Using .get() prevents KeyError. If "year" is missing, it defaults to 2000.
                title = b_data.get("title", "Unknown Title")
                author = b_data.get("author", "Unknown Author")
                isbn = b_data.get("isbn", "Unknown ISBN")
                year = b_data.get("year", 2000) 
                
                book = Book(title, author, isbn, int(year))
                book.is_borrowed = b_data.get("is_borrowed", False)
                
                # Only add if it doesn't already exist (prevents duplicates)
                if not book_system.find_book_by_isbn(book.isbn):
                    book_system.add_book(book)
                
            # Load Members
            for m_data in data.get("members", []):
                name = m_data.get("name", "Unknown")
                mem_id = m_data.get("member_id", "Unknown")
                
                member = Member(name, mem_id)
                
                if not member_system.find_member_by_id(member.member_id):
                    member_system.add_member(member)
                
        except json.JSONDecodeError:
            print("Error reading JSON file. Starting with empty data.")
        except Exception as e:
            print(f"An error occurred while loading data: {e}")