import flet as ft

import components as cp
from services import Database


class NoConfigView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page
        self.route = "/no_config"

        self.__init_components__()
        self.__init_config__()

    def __init_components__(self):
        self.controls = [
            cp.Title("Need Configuration"),
            self.subtitle(),
            cp.SecondaryBtn("Settings", on_click=lambda _: self.page.go("/settings")),
        ]

    def __init_config__(self):
        self.padding = 0
        self.spacing = 60
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER

    def subtitle(self) -> cp.Subtitle:
        store_not_setted = not self.page.client_storage.get("store_initials")
        members_not_setted = len(Database().members) == 0

        v = "You're all set."
        if store_not_setted and members_not_setted:
            v = "First you need to set the store and you need to add at least 1 member."
        elif store_not_setted:
            v = "First you need to set the store name and initials."
        elif members_not_setted:
            v = "First you need to add at least 1 member."
        return cp.Subtitle(v)
