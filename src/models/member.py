# src/models/member.py
class Member:
    """Represents a library member."""
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id

    def to_dict(self):
        """Converts the member object to a dictionary for JSON serialization."""
        return self.__dict__

    @staticmethod
    def from_dict(data):
        """Creates a member object from a dictionary."""
        return Member(**data)