from datetime import date

class Loan:
    """Represents a book loan transaction."""
    def __init__(self, book, member, checkout_date: date, due_date: date):
        self.book = book
        self.member = member
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.return_date = None

    def mark_returned(self, return_date: date):
        self.return_date = return_date