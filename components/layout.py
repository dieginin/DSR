import flet as ft

from .text import Title


class CenteredColumn(ft.Column):
    def __init__(
        self, controls: list[ft.Control] | None = None, expand: bool | int | None = None
    ):
        super().__init__(controls, expand=expand)
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER


class CenteredRow(ft.Row):
    def __init__(
        self, controls: list[ft.Control] | None = None, expand: bool | int | None = None
    ):
        super().__init__(controls, expand=expand)
        self.alignment = ft.MainAxisAlignment.CENTER


class Section(CenteredColumn):
    def __init__(self, title: str, content: ft.Control, expand: bool | None = None):
        super().__init__(expand=expand)
        self.controls = [Title(title), ft.Divider(height=1), content]
