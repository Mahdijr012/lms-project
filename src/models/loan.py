# src/models/loan.py
from datetime import date, timedelta
from src.utils import constants

class Loan:
    """
    Represents the act of a member borrowing a book.
    Connects a Member to a Book with a specific due date.
    """
    def __init__(self, book_isbn, member_id):
        self.book_isbn = book_isbn
        self.member_id = member_id
        self.checkout_date = date.today()
        self.due_date = self.checkout_date + timedelta(days=constants.LOAN_PERIOD_DAYS)
        self.return_date = None # None means it's not returned yet

    def is_overdue(self):
        """Checks if the loan is overdue as of today."""
        return self.return_date is None and date.today() > self.due_date

    def __str__(self):
        status = "Returned" if self.return_date else "Active"
        return f"Loan of ISBN {self.book_isbn} to Member {self.member_id} on {self.checkout_date} - Status: {status}"