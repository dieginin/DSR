import datetime

from .member import Member


class SalesReport:
    def __init__(
        self,
        id: int,
        date: datetime.date,
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
    ):
        self._id = id
        self.date = date
        self.time_open = self.validate_hour(time_open)
        self.time_close = self.validate_hour(time_close)
        self.who_open = who_open
        self.who_close = who_close
        self.gc50 = gc50
        self.gc25 = gc25
        self.ltmns = ltmns
        self.bl100 = bl100
        self.bl50 = bl50
        self.bl20 = bl20
        self.bl10 = bl10
        self.bl05 = bl05
        self.bl02 = bl02
        self.bl01 = bl01
        self.ct25 = ct25
        self.ct10 = ct10
        self.ct05 = ct05
        self.ct01 = ct01
        self.cash_sales = cash_sales
        self.cash_sales_amount = cash_sales_amount
        self.card_sales = card_sales
        self.card_sales_amount = card_sales_amount
        self.gift_sales = gift_sales
        self.gift_sales_amount = gift_sales_amount
        self.cash_returns = cash_returns
        self.cash_returns_amount = cash_returns_amount
        self.card_returns = card_returns
        self.card_returns_amount = card_returns_amount

    @staticmethod
    def validate_hour(hour) -> datetime.time:
        try:
            hour, minute = map(int, hour.split(":"))
            return datetime.time(hour, minute)
        except ValueError:
            return datetime.time(0, 0)

    @property
    def id(self) -> int:
        return self._id

    @property
    def sales(self) -> int:
        card_sales = self.card_sales or 0
        cash_sales = self.cash_sales or 0
        gift_sales = self.gift_sales or 0
        return card_sales + cash_sales + gift_sales

    @property
    def sales_amount(self) -> float:
        card_sales_amount = self.card_sales_amount or 0
        cash_sales_amount = self.cash_sales_amount or 0
        gift_sales_amount = self.gift_sales_amount or 0
        return card_sales_amount + cash_sales_amount + gift_sales_amount

    @property
    def returns(self) -> int:
        card_returns = self.card_returns or 0
        cash_returns = self.cash_returns or 0
        return card_returns + cash_returns

    @property
    def returns_amount(self) -> float:
        card_returns_amount = self.card_returns_amount or 0
        cash_returns_amount = self.cash_returns_amount or 0
        return card_returns_amount + cash_returns_amount

    def __Database(self):
        from services import Database

        return Database()

    def edit(
        self,
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
        return self.__Database().modify_report(
            self,
            time_open,
            time_close,
            who_open,
            who_close,
            gc50,
            gc25,
            ltmns,
            bl100,
            bl50,
            bl20,
            bl10,
            bl05,
            bl02,
            bl01,
            ct25,
            ct10,
            ct05,
            ct01,
            cash_sales,
            cash_sales_amount,
            card_sales,
            card_sales_amount,
            gift_sales,
            gift_sales_amount,
            cash_returns,
            cash_returns_amount,
            card_returns,
            card_returns_amount,
        )

    def close(
        self,
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
        return self.__Database().close_report(
            self,
            gc50,
            gc25,
            ltmns,
            bl100,
            bl50,
            bl20,
            bl10,
            bl05,
            bl02,
            bl01,
            ct25,
            ct10,
            ct05,
            ct01,
            cash_sales,
            cash_sales_amount,
            card_sales,
            card_sales_amount,
            gift_sales,
            gift_sales_amount,
            cash_returns,
            cash_returns_amount,
            card_returns,
            card_returns_amount,
        )
