class Book:
    def __init__(self, title: str, author: str, isbn: str, year: int, total_copies: int = 1):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.total_copies = total_copies
        self.available_copies = total_copies

    def check_out(self):
        if self.available_copies > 0:
            self.available_copies -= 1
            return True
        return False

    def check_in(self):
        if self.available_copies < self.total_copies:
            self.available_copies += 1