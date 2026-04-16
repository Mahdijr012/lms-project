class MemberCollection:
    """ADT for managing registered library members."""
    
    def __init__(self):
        self._members = {} 

    def add_member(self, member):
        if member.member_id in self._members:
            raise ValueError(f"Member ID {member.member_id} already exists!")
        self._members[member.member_id] = member

    def remove_member(self, member_id: str):
        if member_id not in self._members:
            raise KeyError(f"Member ID {member_id} not found.")
            
        member = self._members[member_id]
        if len(member.get_borrowed_books()) > 0:
            raise ValueError("Cannot remove member who has unreturned books.")
        if member.fines_owed > 0:
            raise ValueError("Cannot remove member with outstanding fines.")
            
        del self._members[member_id]

    def find_member_by_id(self, member_id: str):
        return self._members.get(member_id)

    def get_all_members(self):
        return list(self._members.values())