# src/services/loan_service.py
from src.models.loan import Loan
from src.utils import constants

class LoanService:
    """Service for handling the business logic of checking books out and in."""
    def __init__(self, book_collection, member_collection):
        self.book_collection = book_collection
        self.member_collection = member_collection
        self._active_loans = {} # Key: book_isbn, Value: Loan object

    def check_out_book(self, member_id, book_isbn):
        """Checks out a book to a member."""
        member = self.member_collection.find_member_by_id(member_id)
        if not member:
            return False, "Member not found."

        book = self.book_collection.find_book_by_isbn(book_isbn)
        if not book:
            return False, "Book not found."

        # --- Business Rule Checks (as per Module 3) ---
        if book.is_borrowed:
            return False, "Book is already borrowed."
        
        if len(member.borrowed_books_isbns) >= constants.MAX_BORROW_LIMIT:
            return False, "Member has reached the borrowing limit."
        
        # --- Perform the action ---
        book.is_borrowed = True
        member.borrowed_books_isbns.append(book.isbn)
        new_loan = Loan(book_isbn, member_id)
        self._active_loans[book_isbn] = new_loan

        return True, f"Book '{book.title}' checked out to {member.name}."

    def check_in_book(self, book_isbn):
        """Checks in a book."""
        book = self.book_collection.find_book_by_isbn(book_isbn)
        if not book:
            return False, "Book not found."
        
        if not book.is_borrowed:
            return False, "Book is not currently borrowed."

        loan = self._active_loans.get(book_isbn)
        if not loan:
            # This case indicates a data inconsistency, but we'll handle it gracefully
            return False, "Error: Loan record not found for this borrowed book."
        
        member = self.member_collection.find_member_by_id(loan.member_id)

        # --- Perform the action ---
        book.is_borrowed = False
        if member and book.isbn in member.borrowed_books_isbns:
            member.borrowed_books_isbns.remove(book.isbn)
        
        # We can move the loan from active to a historical log here if we want
        del self._active_loans[book_isbn]

        return True, f"Book '{book.title}' returned successfully."