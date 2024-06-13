from datetime import date

import flet as ft

import components as cp
from services import Database
from services.helpers import show_dialog


class HomeView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page
        self.route = "/"

        self.__init_components__()
        self.__init_config__()

    def __init_components__(self):
        self.controls = [self.title(), self.buttons()]

    def __init_config__(self):
        self.padding = 0
        self.spacing = 10
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

    def title(self) -> cp.CenteredColumn:
        title_text = f"{self.page.client_storage.get('store_initials')}\n{self.page.client_storage.get('store_name')}"
        return cp.CenteredColumn(
            [ft.Image("logo.png", width=500), cp.Title(title_text)]
        )

    def buttons(self) -> cp.CenteredColumn:
        db = Database()
        store_opened = bool(db.get_report_by_date(date.today()))
        not_reports = len(db.sales_reports) == 0
        open_btn = cp.CustomBtn(
            "Open Store",
            color="lightgreenaccent",
            icon="countertops_rounded",
            on_click=self.open_store,
            visible=not store_opened,
        )
        close_btn = cp.CustomBtn(
            "Close Store",
            color="redaccent",
            icon="countertops_rounded",
            on_click=self.close_store,
            visible=store_opened,
        )
        count_btn = cp.TertiaryBtn(
            "Count", icon="numbers_rounded", on_click=self.count_money
        )
        view_btn = cp.PrimaryBtn(
            "Search",
            icon="search_rounded",
            on_click=lambda _: self.page.go("/view"),
            disabled=not_reports,
        )
        settings_btn = cp.SecondaryBtn(
            "Settings",
            icon="settings_rounded",
            on_click=lambda _: self.page.go("/settings"),
        )
        return cp.CenteredColumn(
            [open_btn, close_btn, cp.CenteredRow([count_btn, view_btn]), settings_btn]
        )

    def open_store(self, e: ft.ControlEvent):
        def open(self, e: ft.ControlEvent):
            pass

        show_dialog(self.page, "Open Store", ft.Text("Store"), "Open", on_confirm=open)

    def close_store(self, e: ft.ControlEvent):
        def close(self, e: ft.ControlEvent):
            pass

        show_dialog(
            self.page, "Close Store", ft.Text("Store"), "Close", on_confirm=close
        )

    def count_money(self, e: ft.ControlEvent):
        show_dialog(self.page, "Count Money", ft.Text("Store"))
