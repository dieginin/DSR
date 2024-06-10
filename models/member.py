class Member:
    def __init__(
        self,
        id: int,
        name: str,
        initials: str,
        color: str,
    ):
        self._id = id
        self.name = name
        self.initials = initials
        self.color = color

    @property
    def id(self) -> int:
        return self._id

    def __Database(self):
        from services import Database

        return Database()

    def modify(
        self,
        name: str | None = None,
        initials: str | None = None,
        color: str | None = None,
    ) -> str:
        return self.__Database().modify_member(self, name, initials, color)

    def delete(self) -> str:
        return self.__Database().delete_member(self)
