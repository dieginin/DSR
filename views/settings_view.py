import flet as ft

import components as cp
from models import Member
from services import Database, error_snackbar, show_dialog, success_snackbar


class DataTable(ft.DataTable):
    column_names = ["Name", "Initials", "Color", ""]

    def __init__(self):
        super().__init__()
        self.columns = [
            ft.DataColumn(ft.Text(i, color="tertiary", size=15))
            for i in self.column_names
        ]
        self.set_rows()

    def set_rows(self):
        db = Database()
        self.rows.clear()
        for member in db.members:
            self.rows.append(
                ft.DataRow(
                    [
                        ft.DataCell(ft.Text(member.name)),
                        self.make_row(ft.Text(member.initials)),
                        self.make_row(
                            cp.ColorBtn(
                                member.color, show_color=True, callback=self.edit_color
                            ),
                            data=member,
                        ),
                        self.make_row(
                            ft.Row(
                                [
                                    ft.IconButton(
                                        "edit",
                                        on_click=self.edit_member,
                                        style=ft.ButtonStyle(
                                            color="tertiary",
                                            overlay_color="tertiary,.1",
                                        ),
                                    ),
                                    ft.IconButton(
                                        "delete",
                                        on_click=self.delete_member,
                                        style=ft.ButtonStyle(
                                            color="red", overlay_color="red,.1"
                                        ),
                                    ),
                                ],
                                data=member,
                            ),
                            data=member,
                        ),
                    ]
                )
            )

    def make_row(self, content: ft.Control, data=None):
        return ft.DataCell(
            ft.Container(content, alignment=ft.alignment.center), data=data
        )

    def edit_color(self, e: ft.ControlEvent, member: Member, color: str):
        if member.color != color:
            modify = member.modify(color=color)
            if "modified" in modify:
                self.set_rows()
                success_snackbar(e.page, modify)
            else:
                error_snackbar(e.page, modify)

    def edit_member(self, e: ft.ControlEvent):
        member: Member = e.control.parent.data

        def edit(e: ft.ControlEvent):
            name = name_field.value.title().strip() if name_field.value else None
            initials = initials_field.value.strip() if initials_field.value else None

            if name or initials:
                e.page.dialog.close(e)
                edit_result = member.modify(name, initials)

                if "modified" in edit_result:
                    self.set_rows()
                    success_snackbar(e.page, edit_result)
                else:
                    error_snackbar(e.page, edit_result)
            else:
                name_field.focus()

        name_field = cp.TextField(
            member.name, capitalization="word", on_submit=edit, autofocus=True
        )
        initials_field = cp.TextField(
            member.initials,
            capitalization="upper",
            width=80,
            max_length=5,
            on_submit=edit,
        )
        body = ft.Container(cp.CenteredColumn([name_field, initials_field]), height=125)
        show_dialog(e.page, "Edit Member", body, "Edit", edit)

    def delete_member(self, e: ft.ControlEvent):
        member: Member = e.control.parent.data

        def delete(e: ft.ControlEvent):
            e.page.dialog.close(e)
            delete_result = member.delete()

            if "deleted" in delete_result:
                self.parent.parent.parent.parent.__init_components__()  # type: ignore
                success_snackbar(e.page, delete_result)

        body = ft.Text(
            f"Do you really want to delete\n{member.name}?",
            text_align=ft.TextAlign.CENTER,
        )
        show_dialog(e.page, "Delete Member", body, "Delete", delete)


class SettingsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page
        self.route = "/settings"

        self.__init_components__()
        self.__init_config__()

    def __init_components__(self):
        self.divider = "•"
        self.controls = [self.store_section(), self.members_section()]

    def __init_config__(self):
        self.padding = 0
        self.expand = True
        self.floating_action_button = cp.HomeBtn()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def store_section(self) -> cp.Section:
        store = cp.Subtitle(
            f"{self.page.client_storage.get('store_initials')} {self.divider} {self.page.client_storage.get('store_name')}"
        )
        button = cp.IconBtn(
            "edit_rounded", tooltip="Edit Store", on_click=self.edit_store
        )

        return cp.Section(
            "Store",
            cp.CenteredRow([store, button]),
        )

    def members_section(self) -> cp.Section:
        self.new_name = cp.TextField(
            "Name",
            capitalization="word",
            on_change=self.suggest_initials,
            on_submit=self.add_member,
        )
        self.new_initials = cp.TextField(
            "Initials",
            capitalization="upper",
            width=80,
            max_length=5,
            on_submit=self.add_member,
        )
        self.new_color = cp.ColorBtn()

        new_member_row = cp.CenteredRow(
            [
                self.new_name,
                self.new_initials,
                self.new_color,
                cp.PrimaryBtn("Add", on_click=self.add_member),
            ]
        )
        members_table = (
            cp.Subtitle("First add a member")
            if len(Database().members) == 0
            else ft.Column(
                [DataTable()],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            )
        )
        return cp.Section(
            "Members",
            cp.CenteredColumn([new_member_row, members_table], expand=True),
            expand=True,
        )

    def edit_store(self, _):
        def edit_store(e: ft.ControlEvent):
            initials = initials_field.value.strip() if initials_field.value else None
            name = name_field.value.title().strip() if name_field.value else None

            if name and initials:
                e.page.dialog.close(e)
                e.page.client_storage.set("store_initials", initials)
                e.page.client_storage.set("store_name", name)
                self.__init_components__()
                success_snackbar(e.page, f"{initials} {self.divider} {name} setted")
            else:
                if initials:
                    name_field.focus()
                else:
                    initials_field.focus()

        initials_field = cp.TextField(
            "Initials",
            autofocus=True,
            capitalization="upper",
            width=80,
            max_length=5,
            on_submit=edit_store,
        )
        name_field = cp.TextField("Name", capitalization="word", on_submit=edit_store)
        if old_initials := self.page.client_storage.get("store_initials"):
            initials_field.value = old_initials
        if old_name := self.page.client_storage.get("store_name"):
            name_field.value = old_name

        body = ft.Container(cp.CenteredColumn([initials_field, name_field]), height=125)
        show_dialog(self.page, "Edit Store", body, "Edit", edit_store)

    def add_member(self, _):
        name = self.new_name.value.strip() if self.new_name.value else None
        initials = self.new_initials.value.strip() if self.new_initials.value else None
        color = self.new_color.value

        if not name:
            self.new_name.focus()
            error_snackbar(self.page, "First you need to set name, initials and color")
            return
        if not initials:
            self.new_initials.focus()
            error_snackbar(self.page, "First you need to set initials and color")
            return

        add_result = Database().add_member(name, initials, color)
        if "inserted" in add_result:
            self.__init_components__()
            success_snackbar(self.page, add_result)
        else:
            error_snackbar(self.page, add_result)

    def suggest_initials(self, e: ft.ControlEvent):
        name_splited = e.control.value.split()
        initials_suggested = ""
        if len(name_splited) > 1:
            for w in name_splited[:5]:
                initials_suggested += w[0]
        else:
            try:
                initials_suggested = name_splited[0][:2].upper()
            except:
                initials_suggested = initials_suggested

        self.new_initials.value = initials_suggested
        self.new_initials.update()
