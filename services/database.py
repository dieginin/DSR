from datetime import date

from tinydb import Query, TinyDB
from tinydb.table import Document, Table

from models import Member, SalesReport


class Database:
    def __init__(self):
        db = TinyDB("database.json")
        self._members = db.table("members")
        self._sales_reports = db.table("sales_reports")

    def _check_existence(self, table: Table, **kwargs) -> str | None:
        for key, value in kwargs.items():
            if table.search(Query()[key] == value):
                return f"Existing {key}"

    def _insert(self, table: Table, data: dict) -> None:
        id = table.insert({"id": 0, **data})
        table.update({"id": id}, doc_ids=[id])

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

    def get_member_by_id(self, id: int) -> Member:
        search_result = self._members.get(doc_id=id)
        if search_result and type(search_result) == Document:
            return Member(
                search_result["id"],
                search_result["name"],
                search_result["initials"],
                search_result["color"],
            )
        return Member(0, "", "", "")

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
            self._members.update({"name": name}, doc_ids=[member.id])
            member.name = name
        if initials:
            self._members.update({"initials": initials}, doc_ids=[member.id])
            member.initials = initials
        if color:
            self._members.update({"color": color}, doc_ids=[member.id])
            member.color = color
            return f"{member.name} color modified to {member.color}"
        return f"[{member.initials}] {member.name} modified"

    def delete_member(self, member: Member) -> str:
        self._members.remove(doc_ids=[member.id])
        return f"[{member.initials}] {member.name} deleted"

    @property
    def sales_reports(self) -> list[SalesReport]:
        return [
            SalesReport(
                report["id"],
                report["date"],
                report["time_open"],
                report["time_close"],
                self.get_member_by_id(report["who_open"]),
                self.get_member_by_id(report["who_close"]),
                report["gc50"],
                report["gc25"],
                report["ltmns"],
                report["bl100"],
                report["bl50"],
                report["bl20"],
                report["bl10"],
                report["bl05"],
                report["bl02"],
                report["bl01"],
                report["ct25"],
                report["ct10"],
                report["ct05"],
                report["ct01"],
                report.get("cash_sales"),
                report.get("cash_sales_amount"),
                report.get("card_sales"),
                report.get("card_sales_amount"),
                report.get("gift_sales"),
                report.get("gift_sales_amount"),
                report.get("cash_returns"),
                report.get("cash_returns_amount"),
                report.get("card_returns"),
                report.get("card_returns_amount"),
            )
            for report in self._sales_reports.all()
        ]

    def get_report_by_date(self, date: date) -> SalesReport | None:
        for report in self.sales_reports:
            if report.date == date:
                return report

    def add_report(
        self,
        date: date,
        time_open: str,
        time_close: str,
        who_open: Member,
        who_close: Member,
        gc50: int,
        gc25: int,
        ltmns: int,
        bl100: int,
        bl50: int,
        bl20: int,
        bl10: int,
        bl05: int,
        bl02: int,
        bl01: int,
        ct25: int,
        ct10: int,
        ct05: int,
        ct01: int,
    ) -> str:
        if exists := self._check_existence(self._sales_reports, date=date):
            return exists
        self._insert(
            self._sales_reports,
            {
                "date": date,
                "time_open": time_open,
                "time_close": time_close,
                "who_open": who_open.id,
                "who_close": who_close.id,
                "gc50": gc50,
                "gc25": gc25,
                "ltmns": ltmns,
                "bl100": bl100,
                "bl50": bl50,
                "bl20": bl20,
                "bl10": bl10,
                "bl05": bl05,
                "bl02": bl02,
                "bl01": bl01,
                "ct25": ct25,
                "ct10": ct10,
                "ct05": ct05,
                "ct01": ct01,
            },
        )
        return f"{date.strftime('%-d %b %y')} opened"

    def modify_report(
        self,
        sales_report: SalesReport,
        time_open: str | None = None,
        time_close: str | None = None,
        who_open: Member | None = None,
        who_close: Member | None = None,
        gc50: int | None = None,
        gc25: int | None = None,
        ltmns: int | None = None,
        bl100: int | None = None,
        bl50: int | None = None,
        bl20: int | None = None,
        bl10: int | None = None,
        bl05: int | None = None,
        bl02: int | None = None,
        bl01: int | None = None,
        ct25: int | None = None,
        ct10: int | None = None,
        ct05: int | None = None,
        ct01: int | None = None,
        cash_sales: int | None = None,
        cash_sales_amount: float | None = None,
        card_sales: int | None = None,
        card_sales_amount: float | None = None,
        gift_sales: int | None = None,
        gift_sales_amount: float | None = None,
        cash_returns: int | None = None,
        cash_returns_amount: float | None = None,
        card_returns: int | None = None,
        card_returns_amount: float | None = None,
    ) -> str:
        if time_open:
            self._sales_reports.update(
                {"time_open": time_open}, doc_ids=[sales_report.id]
            )
            sales_report.time_open = sales_report.validate_hour(time_open)
        if time_close:
            self._sales_reports.update(
                {"time_close": time_close}, doc_ids=[sales_report.id]
            )
            sales_report.time_close = sales_report.validate_hour(time_close)
        if who_open:
            self._sales_reports.update(
                {"who_open": who_open.id}, doc_ids=[sales_report.id]
            )
            sales_report.who_open = who_open
        if who_close:
            self._sales_reports.update(
                {"who_close": who_close.id}, doc_ids=[sales_report.id]
            )
            sales_report.who_close = who_close
        if gc50:
            self._sales_reports.update({"gc50": gc50}, doc_ids=[sales_report.id])
            sales_report.gc50 = gc50
        if gc25:
            self._sales_reports.update({"gc25": gc25}, doc_ids=[sales_report.id])
            sales_report.gc25 = gc25
        if ltmns:
            self._sales_reports.update({"ltmns": ltmns}, doc_ids=[sales_report.id])
            sales_report.ltmns = ltmns
        if bl100:
            self._sales_reports.update({"bl100": bl100}, doc_ids=[sales_report.id])
            sales_report.bl100 = bl100
        if bl50:
            self._sales_reports.update({"bl50": bl50}, doc_ids=[sales_report.id])
            sales_report.bl50 = bl50
        if bl20:
            self._sales_reports.update({"bl20": bl20}, doc_ids=[sales_report.id])
            sales_report.bl20 = bl20
        if bl10:
            self._sales_reports.update({"bl10": bl10}, doc_ids=[sales_report.id])
            sales_report.bl10 = bl10
        if bl05:
            self._sales_reports.update({"bl05": bl05}, doc_ids=[sales_report.id])
            sales_report.bl05 = bl05
        if bl02:
            self._sales_reports.update({"bl02": bl02}, doc_ids=[sales_report.id])
            sales_report.bl02 = bl02
        if bl01:
            self._sales_reports.update({"bl01": bl01}, doc_ids=[sales_report.id])
            sales_report.bl01 = bl01
        if ct25:
            self._sales_reports.update({"ct25": ct25}, doc_ids=[sales_report.id])
            sales_report.ct25 = ct25
        if ct10:
            self._sales_reports.update({"ct10": ct10}, doc_ids=[sales_report.id])
            sales_report.ct10 = ct10
        if ct05:
            self._sales_reports.update({"ct05": ct05}, doc_ids=[sales_report.id])
            sales_report.ct05 = ct05
        if ct01:
            self._sales_reports.update({"ct01": ct01}, doc_ids=[sales_report.id])
            sales_report.ct01 = ct01
        if cash_sales:
            self._sales_reports.update(
                {"cash_sales": cash_sales}, doc_ids=[sales_report.id]
            )
            sales_report.cash_sales = cash_sales
        if cash_sales_amount:
            self._sales_reports.update(
                {"cash_sales_amount": cash_sales_amount}, doc_ids=[sales_report.id]
            )
            sales_report.cash_sales_amount = cash_sales_amount
        if card_sales:
            self._sales_reports.update(
                {"card_sales": card_sales}, doc_ids=[sales_report.id]
            )
            sales_report.card_sales = card_sales
        if card_sales_amount:
            self._sales_reports.update(
                {"card_sales_amount": card_sales_amount}, doc_ids=[sales_report.id]
            )
            sales_report.card_sales_amount = card_sales_amount
        if gift_sales:
            self._sales_reports.update(
                {"gift_sales": gift_sales}, doc_ids=[sales_report.id]
            )
            sales_report.gift_sales = gift_sales
        if gift_sales_amount:
            self._sales_reports.update(
                {"gift_sales_amount": gift_sales_amount}, doc_ids=[sales_report.id]
            )
            sales_report.gift_sales_amount = gift_sales_amount
        if cash_returns:
            self._sales_reports.update(
                {"cash_returns": cash_returns}, doc_ids=[sales_report.id]
            )
            sales_report.cash_returns = cash_returns
        if cash_returns_amount:
            self._sales_reports.update(
                {"cash_returns_amount": cash_returns_amount}, doc_ids=[sales_report.id]
            )
            sales_report.cash_returns_amount = cash_returns_amount
        if card_returns:
            self._sales_reports.update(
                {"card_returns": card_returns}, doc_ids=[sales_report.id]
            )
            sales_report.card_returns = card_returns
        if card_returns_amount:
            self._sales_reports.update(
                {"card_returns_amount": card_returns_amount}, doc_ids=[sales_report.id]
            )
            sales_report.card_returns_amount = card_returns_amount
        return f"{sales_report.date.strftime('%-d %b %y')} report modified"

    def close_report(
        self,
        sales_report: SalesReport,
        gc50: int,
        gc25: int,
        ltmns: int,
        bl100: int,
        bl50: int,
        bl20: int,
        bl10: int,
        bl05: int,
        bl02: int,
        bl01: int,
        ct25: int,
        ct10: int,
        ct05: int,
        ct01: int,
        cash_sales: int,
        cash_sales_amount: float,
        card_sales: int,
        card_sales_amount: float,
        gift_sales: int,
        gift_sales_amount: float,
        cash_returns: int,
        cash_returns_amount: float,
        card_returns: int,
        card_returns_amount: float,
    ) -> str:
        self._sales_reports.update(
            {
                "gc50": gc50,
                "gc25": gc25,
                "ltmns": ltmns,
                "bl100": bl100,
                "bl50": bl50,
                "bl20": bl20,
                "bl10": bl10,
                "bl05": bl05,
                "bl02": bl02,
                "bl01": bl01,
                "ct25": ct25,
                "ct10": ct10,
                "ct05": ct05,
                "ct01": ct01,
                "cash_sales": cash_sales,
                "cash_sales_amount": cash_sales_amount,
                "card_sales": card_sales,
                "card_sales_amount": card_sales_amount,
                "gift_sales": gift_sales,
                "gift_sales_amount": gift_sales_amount,
                "cash_returns": cash_returns,
                "cash_returns_amount": cash_returns_amount,
                "card_returns": card_returns,
                "card_returns_amount": card_returns_amount,
            },
            doc_ids=[sales_report.id],
        )
        sales_report.gc50 = gc50
        sales_report.gc25 = gc25
        sales_report.ltmns = ltmns
        sales_report.bl100 = bl100
        sales_report.bl50 = bl50
        sales_report.bl20 = bl20
        sales_report.bl10 = bl10
        sales_report.bl05 = bl05
        sales_report.bl02 = bl02
        sales_report.bl01 = bl01
        sales_report.ct25 = ct25
        sales_report.ct10 = ct10
        sales_report.ct05 = ct05
        sales_report.ct01 = ct01
        sales_report.cash_sales = cash_sales
        sales_report.cash_sales_amount = cash_sales_amount
        sales_report.card_sales = card_sales
        sales_report.card_sales_amount = card_sales_amount
        sales_report.gift_sales = gift_sales
        sales_report.gift_sales_amount = gift_sales_amount
        sales_report.cash_returns = cash_returns
        sales_report.cash_returns_amount = cash_returns_amount
        sales_report.card_returns = card_returns
        sales_report.card_returns_amount = card_returns_amount
        return f"{sales_report.date.strftime('%-d %b %y')} closed"
