# src/models/loan.py
from datetime import date

class Loan:
    """Represents the record of a book being loaned to a member."""
    def __init__(self, book_isbn, member_id, checkout_date, due_date, return_date=None):
        self.book_isbn = book_isbn
        self.member_id = member_id
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.return_date = return_date

    def to_dict(self):
        """Converts the Loan object to a dictionary for JSON serialization."""
        return {
            'book_isbn': self.book_isbn,
            'member_id': self.member_id,
            'checkout_date': self.checkout_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else None,
        }

    @staticmethod
    def from_dict(data):
        """Creates a Loan object from a dictionary (from JSON)."""
        return Loan(
            book_isbn=data['book_isbn'],
            member_id=data['member_id'],
            checkout_date=date.fromisoformat(data['checkout_date']),
            due_date=date.fromisoformat(data['due_date']),
            return_date=date.fromisoformat(data['return_date']) if data['return_date'] else None
        )