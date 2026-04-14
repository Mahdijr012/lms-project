class MemberCollection:
    def __init__(self):
        self._members = {}

    def add_member(self, member):
        if member.get_id() in self._members:
            raise ValueError("Member already exists")
        self._members[member.get_id()] = member

    def remove_member(self, member_id):
        if member_id not in self._members:
            raise KeyError("Member not found")
        del self._members[member_id]

    def find_by_id(self, member_id):
        return self._members.get(member_id)

    def find_by_name(self, name):
        return [m for m in self._members.values() if name.lower() in m.get_name().lower()]

    def count(self):
        return len(self._members)

    def get_all(self):
        return list(self._members.values())