from tinydb import Query, TinyDB
from tinydb.table import Table

from models import Member


class Database:
    def __init__(self):
        db = TinyDB("database.json")
        self._members = db.table("members")

    def _check_existence(self, table: Table, **kwargs) -> str | None:
        for key, value in kwargs.items():
            if table.search(Query()[key] == value):
                return f"Existing {key}"
        return

    def _insert(self, table: Table, data: dict) -> None:
        id = table.insert({"id": 0, **data})
        table.update({"id": id}, doc_ids=[id])

    def _update(self, table: Table, id: int, data: dict) -> None:
        table.update(data, doc_ids=[id])

    def _delete(self, table: Table, id: int) -> None:
        table.remove(doc_ids=[id])

    @property
    def members(self) -> list[Member]:
        return sorted(
            [
                Member(
                    member["id"], member["name"], member["initials"], member["color"]
                )
                for member in self._members.all()
                if member
            ],
            key=lambda m: m.name,
        )

    def add_member(self, name: str, initials: str, color: str) -> str:
        if exists := self._check_existence(
            self._members, name=name, initials=initials, color=color
        ):
            return exists

        self._insert(
            self._members, {"name": name, "initials": initials, "color": color}
        )
        return f"[{initials}] {name} inserted"

    def modify_member(
        self,
        member: Member,
        name: str | None = None,
        initials: str | None = None,
        color: str | None = None,
    ) -> str:
        if exists := self._check_existence(
            self._members, name=name, initials=initials, color=color
        ):
            return exists

        if name:
            self._update(self._members, member.id, {"name": name})
            member.name = name
        if initials:
            self._update(self._members, member.id, {"initials": initials})
            member.initials = initials
        if color:
            self._update(self._members, member.id, {"color": color})
            member.color = color
            return f"{member.name} color modified to {member.color}"
        return f"[{member.initials}] {member.name} modified"

    def delete_member(self, member: Member) -> str:
        self._delete(self._members, member.id)
        return f"{member.name} deleted"
