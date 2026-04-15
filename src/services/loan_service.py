# src/services/loan_service.py
import json
from datetime import date, timedelta
from src.models.loan import Loan
from src.utils.constants import LOAN_PERIOD_DAYS

class LoanService:
    """
    Service for handling the business logic of checking books out and in.
    This service manages all active loan records.
    """
    def __init__(self, book_collection, member_collection):
        self.book_collection = book_collection
        self.member_collection = member_collection
        self._loans = {} # Key: book_isbn, Value: active Loan object

    def load_data(self, file_path):
        """Loads active loan data from the 'loans' key in a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                loan_data_list = data.get('loans', [])
                for l_data in loan_data_list:
                    loan = Loan.from_dict(l_data)
                    # Only active loans (not returned) are managed in this dictionary
                    if loan.return_date is None:
                        self._loans[loan.book_isbn] = loan
        except (FileNotFoundError, json.JSONDecodeError):
            self._loans = {}

    def save_data(self, file_path):
        """Saves active loans to the 'loans' key in a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data['loans'] = [loan.to_dict() for loan in self._loans.values()]

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def check_out_book(self, member_id, book_isbn):
        """Checks out a book to a member."""
        member = self.member_collection.find_member_by_id(member_id)
        if not member:
            return False, "Member not found."

        book = self.book_collection.find_book_by_isbn(book_isbn)
        if not book:
            return False, "Book not found."

        if book.is_borrowed:
            return False, "Book is already borrowed."
        
        # --- Create Loan Record ---
        checkout_date = date.today()
        due_date = checkout_date + timedelta(days=LOAN_PERIOD_DAYS) 
        new_loan = Loan(book_isbn, member_id, checkout_date, due_date)
        self._loans[book_isbn] = new_loan
        
        book.is_borrowed = True
        return True, f"Book '{book.title}' checked out to {member.name}."

    def check_in_book(self, book_isbn):
        """Checks in a book."""
        loan = self._loans.get(book_isbn)
        if not loan:
            return False, "This book is not recorded as being on loan."
            
        book = self.book_collection.find_book_by_isbn(book_isbn)
        if not book:
            return False, "Error: Book record not found, data may be inconsistent."
        
        book.is_borrowed = False
        loan.return_date = date.today()
        del self._loans[book_isbn] # Move from active to historical (by removing it)
        
        return True, f"Book '{book.title}' returned successfully."