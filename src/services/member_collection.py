# src/services/member_collection.py
import json
from src.models.member import Member

class MemberCollection:
    """Service for managing library members, including persistence."""
    def __init__(self):
        self._members = {} # Key: Member ID, Value: Member object

    def load_data(self, file_path):
        """Loads member data from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                member_data = data.get('members', [])
                for m_data in member_data:
                    member = Member.from_dict(m_data)
                    self._members[member.member_id] = member
        except (FileNotFoundError, json.JSONDecodeError):
            self._members = {}

    def save_data(self, file_path):
        """Saves all members to a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
            
        data['members'] = [member.to_dict() for member in self._members.values()]

        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def add_member(self, member):
        if member.member_id in self._members:
            return False, "Member with this ID already exists."
        self._members[member.member_id] = member
        return True, "Member registered successfully."

    # THIS IS THE NEW METHOD TO ADD
    def find_member_by_id(self, member_id):
        """Finds and returns a member object by their ID."""
        return self._members.get(member_id)
        
    def delete_member(self, member_id):
        if member_id in self._members:
            del self._members[member_id]
            return True, "Member deleted successfully."
        return False, "Member not found."
        
    def get_all_members(self):
        return list(self._members.values())