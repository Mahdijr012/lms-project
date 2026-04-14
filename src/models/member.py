class Member:
    def __init__(self, name, member_id, contact):
        self._name = name
        self._member_id = member_id
        self._contact = contact
        self._borrowed_books = []

    def borrow_book(self, book):
        if len(self._borrowed_books) >= 5:
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