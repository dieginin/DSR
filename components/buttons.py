import flet as ft


class __ElevatedButton(ft.ElevatedButton):
    def __init__(self, text, icon, on_click, disabled):
        super().__init__()
        self.text = text
        self.icon = icon
        self.on_click = on_click
        self.disabled = disabled

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
    ):
        super().__init__(text, icon, on_click, disabled)
        self.update_style("primary")


class SecondaryBtn(__ElevatedButton):
    def __init__(
        self,
        text: str,
        icon: str | None = None,
        on_click=None,
        disabled: bool | None = None,
    ):
        super().__init__(text, icon, on_click, disabled)
        self.update_style("secondary")


class TertiaryBtn(__ElevatedButton):
    def __init__(
        self,
        text: str,
        icon: str | None = None,
        on_click=None,
        disabled: bool | None = None,
    ):
        super().__init__(text, icon, on_click, disabled)
        self.update_style("tertiary")


class CustomBtn(__ElevatedButton):
    def __init__(
        self,
        text: str,
        color: str,
        icon: str | None = None,
        on_click=None,
        disabled: bool | None = None,
    ):
        super().__init__(text, icon, on_click, disabled)
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
