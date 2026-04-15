class BookCollection:
    """ADT for managing a collection of books."""
    def __init__(self):
        self._books = {} 

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError(f"Book with ISBN {book.isbn} already exists!")
        self._books[book.isbn] = book

    def remove_book(self, isbn: str):
        if isbn not in self._books:
            raise KeyError(f"Book with ISBN {isbn} not found.")
        del self._books[isbn]

    def find_book_by_isbn(self, isbn: str):
        return self._books.get(isbn)

    def find_by_title(self, title_substring: str):
        results = []
        for book in self._books.values():
            if title_substring.lower() in book.title.lower():
                results.append(book)
        return results

    def get_all_books(self):
        return list(self._books.values())