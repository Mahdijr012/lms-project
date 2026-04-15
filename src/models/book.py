# src/models/book.py

class Book:
    """
    Represents a single book in the library. This is a core data model (ADT).
    It encapsulates the book's attributes and state (like is_borrowed).
    """
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        # A book is not borrowed when it's first added
        self.is_borrowed = False

    def __str__(self):
        """Provides a user-friendly string representation of the book."""
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - Status: {status}"