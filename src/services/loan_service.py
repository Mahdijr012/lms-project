from datetime import date, timedelta
from src.models.loan import Loan
from src.utils.constants import MAX_BORROW_LIMIT, LOAN_PERIOD_DAYS
from src.services.fine_calculator import FineCalculator

class LoanService:
    """Coordinates the borrowing, returning, and tracking of books."""
    
    def __init__(self, book_collection, member_collection):
        self.book_catalog = book_collection
        self.member_registry = member_collection
        self.fine_calculator = FineCalculator()
        self.active_loans = []
        self.loan_history = [] # Tracks past loans for reports

    def check_out_book(self, member_id: str, isbn: str):
        book = self.book_catalog.find_book_by_isbn(isbn)
        member = self.member_registry.find_member_by_id(member_id)

        if not book: return False, "Book not found."
        if not member: return False, "Member not found."

        # Advanced Requirements Checks
        if book.available_copies <= 0:
            return False, "No copies available right now."
            
        if len(member.get_borrowed_books()) >= MAX_BORROW_LIMIT:
            return False, f"Member reached maximum borrow limit of {MAX_BORROW_LIMIT}."

        if member.fines_owed > 0:
            return False, f"Cannot borrow. Member owes ${member.fines_owed:.2f} in fines."

        # Create Loan Record
        checkout_date = date.today()
        due_date = checkout_date + timedelta(days=LOAN_PERIOD_DAYS)
        loan = Loan(book, member, checkout_date, due_date)
        
        # Update Statuses
        book.check_out()
        member.borrow_book(book)
        self.active_loans.append(loan)

        return True, f"Success! Due date is {due_date.strftime('%Y-%m-%d')}."

    def check_in_book(self, isbn: str):
        """Returns a book and calculates fines if overdue."""
        # Find the active loan for this book
        for loan in self.active_loans:
            if loan.book.isbn == isbn:
                return_date = date.today()
                loan.mark_returned(return_date)
                
                # Check if it was returned late
                if loan.is_overdue(return_date):
                    days_overdue = (return_date - loan.due_date).days
                    fine = self.fine_calculator.calculate_fine(days_overdue)
                    loan.member.fines_owed += fine  # Add fine to member's account
                
                # Update statuses
                loan.book.check_in()
                loan.member.return_book(loan.book)
                
                # Move from active to history
                self.active_loans.remove(loan)
                self.loan_history.append(loan)
                
                return True, "Book returned successfully."
                
        return False, "Active loan not found for this ISBN."

    def get_overdue_loans(self):
        """For the Reports Dashboard"""
        today = date.today()
        return [loan for loan in self.active_loans if loan.is_overdue(today)]