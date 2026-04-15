# src/services/book_collection.py

class BookCollection:
    """
    Service for managing the library's catalog of books.
    Demonstrates strong encapsulation by hiding the internal dictionary.
    """
    def __init__(self):
        self._books = {}  # Using ISBN as the key for O(1) lookups

    def add_book(self, book):
        if book.isbn in self._books:
            return False, "Book with this ISBN already exists."
        self._books[book.isbn] = book
        return True, "Book added successfully."

    def find_book_by_isbn(self, isbn):
        return self._books.get(isbn)

    def find_books_by_title(self, title_query):
        """Case-insensitive search for books by title."""
        found_books = []
        for book in self._books.values():
            if title_query.lower() in book.title.lower():
                found_books.append(book)
        return found_books
    
    def get_all_books(self):
        """Returns a COPY of the list of all books to prevent external modification."""
        return list(self._books.values())