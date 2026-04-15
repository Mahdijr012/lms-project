# src/services/book_collection.py

import json
from src.models.book import Book

class BookCollection:
    """
    Service for managing the library's catalog of books.

    This class demonstrates High Cohesion and Encapsulation. Its single
    responsibility is to manage the collection of books. It hides the internal
    storage mechanism (a dictionary) and provides clean methods for interacting
    with the data. It also handles its own data persistence.
    """
    def __init__(self):
        self._books = {}  # Key: ISBN (string), Value: Book object

    def load_data(self, file_path):
        """
        Loads book data from the 'books' key in a JSON file.
        This allows multiple services to share the same file safely.
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                book_data_list = data.get('books', [])
                for book_data in book_data_list:
                    book = Book.from_dict(book_data)
                    self._books[book.isbn] = book
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty/corrupted, start with an empty collection.
            self._books = {}

    def save_data(self, file_path):
        """
        Saves the current collection of books to the 'books' key in a JSON file.
        It reads the existing file first to avoid overwriting data from other services.
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}  # Start with an empty dictionary if the file is new or invalid.

        # Update only the 'books' part of the data
        data['books'] = [book.to_dict() for book in self._books.values()]

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def add_book(self, book):
        """Adds a new book to the collection."""
        if book.isbn in self._books:
            return False, "Book with this ISBN already exists."
        self._books[book.isbn] = book
        return True, "Book added successfully."
    
    def find_book_by_isbn(self, isbn):
        """Finds and returns a book object by its ISBN."""
        return self._books.get(isbn)

    def get_all_books(self):
        """
        Returns a list of all book objects in the collection.
        This is used by the GUI to display the catalog.
        """
        return list(self._books.values())

    def delete_book(self, isbn):
        """Deletes a book from the collection by its ISBN."""
        # Add a check here to ensure the book isn't currently borrowed
        # before allowing deletion. This would require access to LoanService.
        # For now, we will keep it simple.
        if isbn in self._books:
            del self._books[isbn]
            return True, "Book deleted successfully."
        return False, "Book not found."