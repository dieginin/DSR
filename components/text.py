import flet as ft


class Title(ft.Text):
    def __init__(self, value: str | None = None):
        super().__init__(value, text_align=ft.TextAlign.CENTER)
        self.style = ft.TextStyle(
            size=60,
            weight=ft.FontWeight.W_100,
            letter_spacing=5,
            foreground=ft.Paint(
                gradient=ft.PaintLinearGradient(
                    (0, 135), (120, 20), ["primary", "tertiary"]
                ),
            ),
        )


class Subtitle(ft.Text):
    def __init__(self, value: str | None = None):
        super().__init__(value, text_align=ft.TextAlign.CENTER)
        self.style = ft.TextStyle(
            size=45,
            weight=ft.FontWeight.W_100,
            color="secondary",
            letter_spacing=3,
        )
