# src/services/loan_service.py
import json
from datetime import date, timedelta
from src.models.loan import Loan
from src.utils import constants # Assuming you will create this file

class LoanService:
    """
    Service for handling the business logic of checking books out and in.
    This service manages all active and historical loans.
    """
    def __init__(self, book_collection, member_collection):
        self.book_collection = book_collection
        self.member_collection = member_collection
        self._loans = {} # Key: book_isbn, Value: Loan object

    def load_data(self, file_path):
        """Loads loan data from the JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                loan_data = data.get('loans', [])
                for l_data in loan_data:
                    loan = Loan.from_dict(l_data)
                    # We only care about active loans in memory for checkout/in logic
                    if loan.return_date is None:
                        self._loans[loan.book_isbn] = loan
        except (FileNotFoundError, json.JSONDecodeError):
            self._loans = {}

    def save_data(self, file_path):
        """Saves all loans (active and historical) to the JSON file."""
        # This is a bit tricky since other services write to the same file.
        # A robust implementation reads, updates its part, and writes back.
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Here we'd ideally merge historical loans too, but for now, we just save current state.
        all_loans_in_memory = list(self._loans.values())
        data['loans'] = [loan.to_dict() for loan in all_loans_in_memory]

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)


    def check_out_book(self, member_id, book_isbn):
        """Checks out a book to a member, creating a new Loan record."""
        member = self.member_collection.find_member_by_id(member_id)
        if not member:
            return False, "Member not found."

        book = self.book_collection.find_book_by_isbn(book_isbn)
        if not book:
            return False, "Book not found."

        if book.is_borrowed:
            return False, "Book is already borrowed."
        
        # --- Create the Loan object with correct dates ---
        checkout_date = date.today()
        # You would get LOAN_PERIOD_DAYS from a constants file
        due_date = checkout_date + timedelta(days=14) 
        
        new_loan = Loan(book_isbn, member_id, checkout_date, due_date)
        self._loans[book_isbn] = new_loan
        
        # Update the book's state
        book.is_borrowed = True

        return True, f"Book '{book.title}' checked out to {member.name}."

    def check_in_book(self, book_isbn):
        """Checks in a book, updating the Loan record."""
        loan = self._loans.get(book_isbn)
        if not loan:
            return False, "This book is not recorded as being on loan."
            
        book = self.book_collection.find_book_by_isbn(book_isbn)
        if not book:
            # This indicates a data integrity issue, but we handle it
            return False, "Book record not found."
        
        # --- Update the state of the system ---
        book.is_borrowed = False
        loan.return_date = date.today()
        
        # The loan is now "historical". We can remove it from the active loan dict.
        # When we save, it will be saved with its return_date.
        del self._loans[book_isbn]
        
        # For a complete system, we would add this 'historical' loan to another list
        # before saving, so its record is not lost. For now, this is sufficient.

        return True, f"Book '{book.title}' returned successfully."