import flet as ft


class NoConfigView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page
        self.route = "/no_config"

        self.__init_components__()
        self.__init_config__()

    def __init_components__(self):
        self.controls = []

    def __init_config__(self):
        self.padding = 0
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.SPACE_EVENLY
