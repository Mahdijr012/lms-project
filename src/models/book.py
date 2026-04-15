# src/models/book.py
class Book:
    """Represents a book in the library's collection."""
    def __init__(self, title, author, isbn, is_borrowed=False):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = is_borrowed

    def to_dict(self):
        """Converts the book object to a dictionary for JSON serialization."""
        return self.__dict__

    @staticmethod
    def from_dict(data):
        """Creates a book object from a dictionary."""
        return Book(**data)