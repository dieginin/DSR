import flet as ft

from views import *

from . import Database

routes = {
    "/": HomeView,
    "/no_config": NoConfigView,
    "/settings": SettingsView,
    "/view": ViewView,
}


class Router:
    def __init__(self, page: ft.Page):
        page.on_route_change = self.on_route_change
        page.go("/")

    def on_route_change(self, e: ft.RouteChangeEvent):
        store_initials = e.page.client_storage.get("store_initials")
        needs_configuration = not store_initials or len(Database().members) == 0
        e.page.views.clear()
        if needs_configuration and e.route != "/settings":
            e.page.views.append(routes["/no_config"](e.page))
        else:
            e.page.views.append(routes[e.route](e.page))
        e.page.update()
