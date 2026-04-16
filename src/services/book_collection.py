class BookCollection:
    """ADT for managing the library's catalog of books."""
    
    def __init__(self):
        self._books = {} 

    def add_book(self, book):
        if book.isbn in self._books:
            raise ValueError(f"Book with ISBN {book.isbn} already exists!")
        self._books[book.isbn] = book

    def remove_book(self, isbn: str):
        if isbn not in self._books:
            raise KeyError(f"Book with ISBN {isbn} not found.")
        # Only allow deleting if all copies are in the library
        if self._books[isbn].available_copies < self._books[isbn].total_copies:
            raise ValueError("Cannot delete book. Copies are currently checked out.")
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