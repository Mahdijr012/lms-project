# src/models/loan.py
from datetime import date

class Loan:
    """
    Represents the record of a book being loaned to a member.

    This class is a pure data model (or ADT). It does not calculate its own
    due date; that business logic belongs in the LoanService. It simply
    stores the state of a loan transaction.
    """
    def __init__(self, book_isbn, member_id, checkout_date, due_date, return_date=None):
        self.book_isbn = book_isbn
        self.member_id = member_id
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.return_date = return_date  # None means the loan is still active

    def to_dict(self):
        """
        Converts the Loan object to a dictionary for JSON serialization.
        Date objects are converted to ISO 8601 string format (YYYY-MM-DD).
        """
        return {
            'book_isbn': self.book_isbn,
            'member_id': self.member_id,
            'checkout_date': self.checkout_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Loan object from a dictionary (loaded from JSON).
        Converts date strings back into date objects.
        """
        return Loan(
            book_isbn=data['book_isbn'],
            member_id=data['member_id'],
            checkout_date=date.fromisoformat(data['checkout_date']),
            due_date=date.fromisoformat(data['due_date']),
            return_date=date.fromisoformat(data['return_date']) if data['return_date'] else None
        )

    def is_overdue(self):
        """
        Checks if the loan is overdue as of today's date.
        A loan is overdue if it is not returned and today is past the due date.
        """
        return self.return_date is None and date.today() > self.due_date

    def __str__(self):
        """Provides a user-friendly string representation of the loan."""
        status = f"Returned on {self.return_date}" if self.return_date else "Active"
        return f"Loan: ISBN '{self.book_isbn}' to Member '{self.member_id}' on {self.checkout_date} [Status: {status}]"