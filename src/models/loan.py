from datetime import datetime, timedelta

class Loan:
    def __init__(self, book, member):
        self._book = book
        self._member = member
        self._borrow_date = datetime.now()
        self._due_date = self._borrow_date + timedelta(days=14)
        self._returned = False

    def return_book(self):
        self._returned = True

    def is_overdue(self):
        return datetime.now() > self._due_date and not self._returned

    def calculate_fine(self):
        if not self.is_overdue():
            return 0
        days = (datetime.now() - self._due_date).days
        return days * 0.5