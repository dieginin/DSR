import random

import flet as ft
from flet_contrib.color_picker import ColorPicker

from .utils import Dialog


class __ElevatedButton(ft.ElevatedButton):
    def __init__(self, text, icon, on_click, disabled, visible):
        super().__init__()
        self.text = text
        self.icon = icon
        self.on_click = on_click
        self.disabled = disabled
        self.visible = visible

    def update_style(self, color: str | None = None):
        color = color if color else self.color
        self.style = ft.ButtonStyle(
            color="outlinevariant" if self.disabled else color,
            surface_tint_color=color,
            overlay_color=f"{color},.1",
        )


class PrimaryBtn(__ElevatedButton):
    def __init__(
        self,
        text: str,
        icon: str | None = None,
        on_click=None,
        disabled: bool | None = None,
        visible: bool | None = None,
    ):
        super().__init__(text, icon, on_click, disabled, visible)
        self.update_style("primary")


class SecondaryBtn(__ElevatedButton):
    def __init__(
        self,
        text: str,
        icon: str | None = None,
        on_click=None,
        disabled: bool | None = None,
        visible: bool | None = None,
    ):
        super().__init__(text, icon, on_click, disabled, visible)
        self.update_style("secondary")


class TertiaryBtn(__ElevatedButton):
    def __init__(
        self,
        text: str,
        icon: str | None = None,
        on_click=None,
        disabled: bool | None = None,
        visible: bool | None = None,
    ):
        super().__init__(text, icon, on_click, disabled, visible)
        self.update_style("tertiary")


class CustomBtn(__ElevatedButton):
    def __init__(
        self,
        text: str,
        color: str,
        icon: str | None = None,
        on_click=None,
        disabled: bool | None = None,
        visible: bool | None = None,
    ):
        super().__init__(text, icon, on_click, disabled, visible)
        self.update_style(color)


class IconBtn(ft.IconButton):
    def __init__(
        self,
        icon: str,
        color: str | None = "tertiary",
        icon_size: ft.OptionalNumber = 30,
        tooltip: str | None = None,
        on_click=None,
        disabled: bool | None = None,
    ):
        super().__init__(
            icon,
            icon_size=icon_size,
            tooltip=tooltip,
            on_click=on_click,
            disabled=disabled,
        )
        self.color = color
        self.highlight_color = f"{color},.2"
        self.hover_color = f"{color},.1"
        self.update_style()

    def update_style(self):
        self.icon_color = "outlinevariant" if self.disabled else self.color


class HomeBtn(ft.FloatingActionButton):
    def __init__(self):
        super().__init__()
        self.icon = "home"
        self.on_click = lambda e: e.page.go("/")


class ColorBtn(ft.ElevatedButton):
    def __init__(
        self, value: str | None = None, show_color: bool = False, callback=None
    ):
        super().__init__()
        self.value = value if value else "#%06x" % random.randint(0, 0xFFFFFF)
        self.tooltip = self.value if show_color else "Set Color"
        self.width = 25
        self.height = 25
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10), bgcolor=self.value
        )
        self.on_click = self._open_dialog
        self.__callback = callback

    def generate_color(self) -> str:
        self.value = "#%06x" % random.randint(0, 0xFFFFFF)
        self.style = ft.ButtonStyle(bgcolor=self.value)
        return self.value

    def _open_dialog(self, e: ft.ControlEvent):
        self._picker = ColorPicker(self.value)
        self._dialog = Dialog(
            "Choose a Color", "Choose", self._picker, on_confirm=self._update_button
        )

        e.page.dialog = self._dialog
        self._dialog.open = True
        e.page.update()

    def _update_button(self, e: ft.ControlEvent):
        if self.__callback:
            if self.__callback(e, self.parent.parent.data, self._picker.color):  # type: ignore
                self.value = self._picker.color
                self.bgcolor = self._picker.color
        else:
            self.value = self._picker.color
            self.bgcolor = self._picker.color
        self._dialog.open = False
        e.page.update()
