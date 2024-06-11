import flet as ft

import components as cp


def show_snackbar(
    page: ft.Page,
    message: str,
    message_color: str | None = None,
    bgcolor: str | None = None,
):
    page.snack_bar = ft.SnackBar(ft.Text(message, color=message_color), bgcolor=bgcolor)
    page.snack_bar.open = True
    page.update()


def show_dialog(
    page: ft.Page,
    title: str,
    content: ft.Control,
    confirm_text: str | None = "Confirm",
    on_confirm=None,
):
    page.dialog = cp.Dialog(title, confirm_text, content, on_confirm)
    page.dialog.open = True
    page.update()
