from datetime import date, timedelta
from src.models.loan import Loan
from src.utils.constants import MAX_BORROW_LIMIT, LOAN_PERIOD_DAYS

class LoanService:
    """Coordinates the borrowing and returning of books."""
    def __init__(self, book_collection, member_collection):
        self.book_catalog = book_collection
        self.member_registry = member_collection
        self.active_loans = []

    def check_out_book(self, member_id: str, isbn: str):
        book = self.book_catalog.find_book_by_isbn(isbn)
        if not book:
            return False, "Book not found."
            
        member = self.member_registry.find_member_by_id(member_id)
        if not member:
            return False, "Member not found."

        if book.is_borrowed:
            return False, "Book is already checked out."
            
        if len(member.get_borrowed_books()) >= MAX_BORROW_LIMIT:
            return False, "Member reached maximum borrow limit."

        checkout_date = date.today()
        due_date = checkout_date + timedelta(days=LOAN_PERIOD_DAYS)
        loan = Loan(book, member, checkout_date, due_date)
        
        book.check_out()
        member.borrow_book(book)
        self.active_loans.append(loan)

        return True, "Book checked out successfully."

    def check_in_book(self, isbn: str):
        book = self.book_catalog.find_book_by_isbn(isbn)
        if not book:
            return False, "Book not found in catalog."
            
        if not book.is_borrowed:
            return False, "Book is not currently borrowed."

        # Find the loan and the member
        for loan in self.active_loans:
            if loan.book.isbn == isbn and loan.return_date is None:
                loan.mark_returned(date.today())
                book.check_in()
                loan.member.return_book(book)
                return True, "Book returned successfully."
                
        return False, "Active loan record not found."