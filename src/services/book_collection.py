class BookCollection:
    def __init__(self):
        self._books = {}

    def add_book(self, book):
        self._books[book.get_isbn()] = book

    def find_by_isbn(self, isbn):
        return self._books.get(isbn)

    def get_all_books(self):
        return list(self._books.values())
