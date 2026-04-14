class Book:
    def __init__(self, title, author, isbn, year):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._year = year
        self._is_borrowed = False

    def borrow(self):
        if not self._is_borrowed:
            self._is_borrowed = True
            return True
        return False

    def return_book(self):
        self._is_borrowed = False

    def is_available(self):
        return not self._is_borrowed

    def get_info(self):
        return f"{self._title} by {self._author}"

    def get_isbn(self):
        return self._isbn