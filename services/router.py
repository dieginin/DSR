import flet as ft

from views import *

routes = {
    "/": HomeView,
    "/no_config": NoConfigView,
    "/settings": SettingsView,
    "/view": ViewView,
}


class Router:
    def __init__(self, page: ft.Page):
        self.__init_route__(page)

    def __init_route__(self, page: ft.Page):
        page.on_route_change = self.on_route_change
        page.go("/")

    def on_route_change(self, e: ft.RouteChangeEvent):
        e.page.views.clear()
        e.page.views.append(routes[e.route](e.page))
        e.page.update()
