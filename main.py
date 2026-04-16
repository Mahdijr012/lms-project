import tkinter as tk
import json
import os
from datetime import datetime

# --- Backend Imports ---
from src.models.member import Member
from src.models.book import Book
from src.models.loan import Loan
from src.services.member_collection import MemberCollection
from src.services.book_collection import BookCollection
from src.services.loan_service import LoanService

# --- GUI Import ---
from gui import LibraryDashboard

DATA_FILE = "library_data.json"
DATE_FORMAT = "%Y-%m-%d"

def load_data(book_system, member_system, loan_system):
    if not os.path.exists(DATA_FILE): return
    with open(DATA_FILE, "r") as file:
        try:
            data = json.load(file)
            
            # Load Books
            for b_data in data.get("books", []):
                copies = b_data.get("total_copies", 1)
                book = Book(b_data.get("title", ""), b_data.get("author", ""), b_data.get("isbn", ""), b_data.get("year", 2000), copies)
                book.available_copies = b_data.get("available_copies", copies)
                try: book_system.add_book(book)
                except ValueError: pass

            # Load Members
            for m_data in data.get("members", []):
                member = Member(m_data.get("name", ""), m_data.get("member_id", ""))
                member.fines_owed = m_data.get("fines_owed", 0.0)
                try: member_system.add_member(member)
                except ValueError: pass

            # Load Active Loans
            for l_data in data.get("active_loans", []):
                book = book_system.find_book_by_isbn(l_data["isbn"])
                member = member_system.find_member_by_id(l_data["member_id"])
                if book and member:
                    checkout_date = datetime.strptime(l_data["checkout_date"], DATE_FORMAT).date()
                    due_date = datetime.strptime(l_data["due_date"], DATE_FORMAT).date()
                    
                    loan = Loan(book, member, checkout_date, due_date)
                    loan_system.active_loans.append(loan)
                    # Re-link the book to the member's borrowed list
                    member._borrowed_books.append(book)

        except Exception as e: print(f"Load Error: {e}")

def save_data(book_system, member_system, loan_system):
    data = {"books": [], "members": [], "active_loans": []}
    
    for b in book_system.get_all_books():
        data["books"].append({
            "title": b.title, "author": b.author, "isbn": b.isbn, 
            "year": b.year, "total_copies": b.total_copies, "available_copies": b.available_copies
        })
        
    for m in member_system.get_all_members():
        data["members"].append({"name": m.name, "member_id": m.member_id, "fines_owed": m.fines_owed})
        
    for loan in loan_system.active_loans:
        data["active_loans"].append({
            "isbn": loan.book.isbn,
            "member_id": loan.member.member_id,
            "checkout_date": loan.checkout_date.strftime(DATE_FORMAT),
            "due_date": loan.due_date.strftime(DATE_FORMAT)
        })
        
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def main():
    root = tk.Tk()
    
    # Initialize Systems
    books = BookCollection()
    members = MemberCollection()
    loans = LoanService(books, members)

    # Load Database
    load_data(books, members, loans)

    # Launch Dashboard
    app = LibraryDashboard(root, books, members, loans)

    # Start Program
    root.mainloop()
    
    # Save Database on exit
    save_data(books, members, loans)

if __name__ == "__main__":
    main()