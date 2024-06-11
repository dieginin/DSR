from typing import Literal

import flet as ft


class Dialog(ft.AlertDialog):
    def __init__(
        self,
        title: str | None = None,
        confirm_text: str | None = "Confirm",
        content: ft.Control | None = None,
        on_confirm=None,
    ):
        super().__init__()
        self.title = ft.Text(title) if title else None
        self.content = content
        self.actions = [
            ft.TextButton(confirm_text, on_click=on_confirm),
            ft.TextButton(
                "Cancel",
                on_click=self.close,
                style=ft.ButtonStyle(color="red", overlay_color="red,.1"),
            ),
        ]

    def close(self, e: ft.ControlEvent):
        self.open = False
        e.page.update()


class TextField(ft.TextField):
    def __init__(
        self,
        hint_text: str | None = None,
        max_length: int | None = None,
        on_submit=None,
        on_change=None,
        autofocus: bool | None = None,
        capitalization: Literal["word", "upper"] | None = None,
        width: ft.OptionalNumber = None,
    ):
        super().__init__()
        self.hint_text = hint_text
        self.max_length = max_length
        self.counter_text = " "
        self.on_submit = on_submit
        self.on_change = on_change
        self.autofocus = autofocus
        self.capitalization = (
            ft.TextCapitalization.CHARACTERS
            if capitalization == "upper"
            else ft.TextCapitalization.WORDS if capitalization == "word" else None
        )  # type: ignore
        self.width = width
        self.border = ft.InputBorder.UNDERLINE
        self.text_align = ft.TextAlign.CENTER
        self.color = "tertiary"
        self.cursor_color = "tertiary"
        self.border_color = "tertiary"
        self.selection_color = "tertiary,.3"
