# src/models/member.py

class Member:
    """
    Represents a single library member. This is another core data model (ADT).
    It encapsulates member information and their relationship with books (borrowed_books).
    """
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        # We will store the ISBNs of the books the member has borrowed
        self.borrowed_books_isbns = []

    def __str__(self):
        """Provides a user-friendly string representation of the member."""
        return f"Member: {self.name} (ID: {self.member_id}), Borrowed: {len(self.borrowed_books_isbns)} books"