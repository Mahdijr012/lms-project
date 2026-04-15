# src/models/book.py

class Book:
    """Represents a single book with methods for JSON serialization."""
    def __init__(self, title, author, isbn, is_borrowed=False):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_borrowed = is_borrowed

    def to_dict(self):
        """Converts the book object to a dictionary."""
        return self.__dict__

    @staticmethod
    def from_dict(data):
        """Creates a book object from a dictionary."""
        return Book(**data)

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {status}"