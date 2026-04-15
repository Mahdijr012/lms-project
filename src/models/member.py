# src/models/member.py

class Member:
    """Represents a library member with methods for JSON serialization."""
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id

    def to_dict(self):
        """Converts the member object to a dictionary."""
        return self.__dict__

    @staticmethod
    def from_dict(data):
        """Creates a member object from a dictionary."""
        return Member(**data)

    def __str__(self):
        return f"{self.name} (ID: {self.member_id})"