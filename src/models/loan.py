from datetime import date

class Loan:
    """
    Represents a book loan transaction.
    Tracks when a member borrows a book, when it's due, and when it's returned.
    """
    
    def __init__(self, book, member, checkout_date: date, due_date: date):
        # We store the actual Book and Member objects, not just their IDs
        self.book = book
        self.member = member
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.return_date = None  # None means the book has not been returned yet

    def is_overdue(self, current_date: date) -> bool:
        """
        Check if the loan is overdue based on a given date.
        (Requirement from Page 8 of the PDF)
        """
        # If it hasn't been returned AND the current date is past the due date
        return self.return_date is None and current_date > self.due_date

    def mark_returned(self, return_date: date):
        """
        Record the date the book was actually returned.
        (Requirement from Page 8 of the PDF)
        """
        self.return_date = return_date