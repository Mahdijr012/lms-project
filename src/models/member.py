class Member:
    """Represents a library member."""
    def __init__(self, name: str, member_id: str):
        self.name = name
        self.member_id = member_id
        self._borrowed_books = []  # Hidden implementation

    def borrow_book(self, book):
        self._borrowed_books.append(book)

    def return_book(self, book):
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)

    def get_borrowed_books(self):
        return self._borrowed_books.copy()