class MemberCollection:
    """ADT for managing a collection of library members."""
    def __init__(self):
        self._members = {} 

    def add_member(self, member):
        if member.member_id in self._members:
            raise ValueError(f"Member ID {member.member_id} already exists!")
        self._members[member.member_id] = member

    def remove_member(self, member_id: str):
        if member_id not in self._members:
            raise KeyError(f"Member ID {member_id} not found.")
        del self._members[member_id]

    def find_member_by_id(self, member_id: str):
        return self._members.get(member_id)

    def get_all_members(self):
        return list(self._members.values())