# src/services/book_collection.py
import json
from src.models.book import Book

class BookCollection:
    """Service for managing the library's catalog of books."""
    def __init__(self):
        self._books = {}  # Key: ISBN, Value: Book object

    def load_data(self, file_path):
        """Loads book data from the 'books' key in a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                book_data_list = data.get('books', [])
                for book_data in book_data_list:
                    book = Book.from_dict(book_data)
                    self._books[book.isbn] = book
        except (FileNotFoundError, json.JSONDecodeError):
            self._books = {}

    def save_data(self, file_path, existing_data):
        """Saves the current book collection into a larger data dictionary."""
        existing_data['books'] = [book.to_dict() for book in self._books.values()]

    def add_book(self, book):
        if book.isbn in self._books:
            return False, "Book with this ISBN already exists."
        self._books[book.isbn] = book
        return True, "Book added successfully."
    
    def find_book_by_isbn(self, isbn):
        return self._books.get(isbn)

    def get_all_books(self):
        return list(self._books.values())

    def delete_book(self, isbn):
        book = self.find_book_by_isbn(isbn)
        if not book:
            return False, "Book not found."
        if book.is_borrowed:
            return False, "Cannot delete a book that is currently borrowed."
        del self._books[isbn]
        return True, "Book deleted successfully."