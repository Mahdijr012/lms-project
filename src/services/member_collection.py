class MemberCollection:
    def __init__(self):
        self._members = {}

    def add_member(self, member):
        self._members[member.get_id()] = member

    def find_by_id(self, member_id):
        return self._members.get(member_id)

    def get_all_members(self):
        return list(self._members.values())