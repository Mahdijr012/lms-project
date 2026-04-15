
class MemberCollection:
    """Service for managing library members."""
    def __init__(self):
        self._members = {}  # Using member_id as the key

    def add_member(self, member):
        if member.member_id in self._members:
            return False, "Member with this ID already exists."
        self._members[member.member_id] = member
        return True, "Member added successfully."

    def find_member_by_id(self, member_id):
        return self._members.get(member_id)

    def get_all_members(self):
        return list(self._members.values())