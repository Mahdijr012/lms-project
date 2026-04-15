# src/services/loan_service.py
import json
from datetime import date, timedelta
from src.models.loan import Loan
# Note: You need to create the constants.py file for this to work
from src.utils.constants import LOAN_PERIOD_DAYS

class LoanService:
    """Service for handling the logic of borrowing and returning books."""
    def __init__(self, book_collection, member_collection):
        self.book_collection = book_collection
        self.member_collection = member_collection
        self._loans = []  # A list to store all loans (active and historical)

    def load_data(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                loan_data_list = data.get('loans', [])
                self._loans = [Loan.from_dict(l_data) for l_data in loan_data_list]
        except (FileNotFoundError, json.JSONDecodeError):
            self._loans = []

    def save_data(self, file_path, existing_data):
        existing_data['loans'] = [loan.to_dict() for loan in self._loans]

    def check_out_book(self, member_id, book_isbn):
        member = self.member_collection.find_member_by_id(member_id)
        if not member:
            return False, "Member not found."

        book = self.book_collection.find_book_by_isbn(book_isbn)
        if not book:
            return False, "Book not found."

        if book.is_borrowed:
            return False, "Book is already borrowed."
        
        checkout_date = date.today()
        due_date = checkout_date + timedelta(days=LOAN_PERIOD_DAYS)
        new_loan = Loan(book_isbn, member_id, checkout_date, due_date)
        self._loans.append(new_loan)
        
        book.is_borrowed = True
        return True, f"Book '{book.title}' checked out to {member.name}."

    def check_in_book(self, book_isbn):
        book = self.book_collection.find_book_by_isbn(book_isbn)
        if not book:
            return False, "Book not found."
        
        if not book.is_borrowed:
            return False, "This book is not currently borrowed."

        # Find the active loan for this book
        active_loan = None
        for loan in self._loans:
            if loan.book_isbn == book_isbn and loan.return_date is None:
                active_loan = loan
                break
        
        if not active_loan:
            return False, "Error: No active loan record found for this book."
        
        active_loan.return_date = date.today()
        book.is_borrowed = False
        return True, f"Book '{book.title}' returned successfully."