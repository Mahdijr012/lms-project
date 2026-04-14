class Member:
    MAX_BORROW_LIMIT = 5

    def __init__(self, name, member_id, contact):
        self._name = name
        self._member_id = member_id
        self._contact = contact
        self._borrowed_books = []
        self._fines = 0.0

    def borrow_book(self, book):
        if len(self._borrowed_books) >= self.MAX_BORROW_LIMIT:
            return False
        if book.borrow():
            self._borrowed_books.append(book)
            return True
        return False

    def return_book(self, book):
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)
            book.return_book()
            return True
        return False

    def get_borrowed_books(self):
        return self._borrowed_books.copy()

    def get_id(self):
        return self._member_id

    def get_name(self):
        return self._name

    def add_fine(self, amount):
        self._fines += amount

    def get_fines(self):
        return self._fines