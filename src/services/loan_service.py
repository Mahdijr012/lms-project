from src.models.loan import Loan

class LoanService:
    def __init__(self):
        self._loans = []

    def borrow_book(self, member, book):
        if member.borrow_book(book):
            loan = Loan(book, member)
            self._loans.append(loan)
            return True
        return False

    def return_book(self, member, book):
        for loan in self._loans:
            if loan._book == book and loan._member == member:
                loan.return_book()
                fine = loan.calculate_fine()
                member.add_fine(fine)
                member.return_book(book)
                return fine
        return 0

    def get_loans(self):
        return list(self._loans)
