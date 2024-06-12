import flet as ft

from services import Router


class Main:
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page

        self.__init_config__()
        self.__init_window__()

    def __init_config__(self):
        self.page.title = "SBM • Daily Sales Report"
        self.page.theme_mode = ft.ThemeMode.DARK
        Router(self.page)

    def __init_window__(self):
        self.page.window_height = self.page.window_min_height = 600
        self.page.window_width = self.page.window_min_width = 800
        self.page.window_center()


ft.app(Main)
