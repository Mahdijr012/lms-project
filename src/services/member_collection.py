# src/services/member_collection.py
import json
from src.models.member import Member

class MemberCollection:
    """Service for managing library members."""
    def __init__(self):
        self._members = {}  # Key: Member ID, Value: Member object

    def load_data(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                member_data_list = data.get('members', [])
                for member_data in member_data_list:
                    member = Member.from_dict(member_data)
                    self._members[member.member_id] = member
        except (FileNotFoundError, json.JSONDecodeError):
            self._members = {}

    def save_data(self, file_path, existing_data):
        existing_data['members'] = [member.to_dict() for member in self._members.values()]

    def add_member(self, member):
        if member.member_id in self._members:
            return False, "Member with this ID already exists."
        self._members[member.member_id] = member
        return True, "Member registered successfully."

    def find_member_by_id(self, member_id):
        return self._members.get(member_id)

    def delete_member(self, member_id):
        if member_id in self._members:
            del self._members[member_id]
            return True, "Member deleted successfully."
        return False, "Member not found."

    def get_all_members(self):
        return list(self._members.values())