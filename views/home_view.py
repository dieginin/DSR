import flet as ft

import components as cp


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
        store_opened = False
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
            "Search", icon="search_rounded", on_click=self.view_report
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
        pass

    def close_store(self, e: ft.ControlEvent):
        pass

    def count_money(self, e: ft.ControlEvent):
        pass

    def view_report(self, e: ft.ControlEvent):
        e.page.go("/view")
