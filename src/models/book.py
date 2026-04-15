class Book:
    """Represents a book and its basic attributes."""
    def __init__(self, title: str, author: str, isbn: str, year: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.is_borrowed = False

    def check_out(self):
        self.is_borrowed = True

    def check_in(self):
        self.is_borrowed = False