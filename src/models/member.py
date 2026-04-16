class Member:
    def __init__(self, name: str, member_id: str):
        self.name = name
        self.member_id = member_id
        self._borrowed_books = []
        self._borrowing_history = [] # Tracks all past loans
        self.fines_owed = 0.0

    def borrow_book(self, book):
        self._borrowed_books.append(book)
        self._borrowing_history.append(book.title)

    def return_book(self, book):
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)

    def get_borrowed_books(self):
        return self._borrowed_books.copy()