import flet as ft

import components as cp
from services import Database, error_snackbar, show_dialog, success_snackbar


class SettingsView(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page: ft.Page = page
        self.route = "/settings"

        self.__init_components__()
        self.__init_config__()

    def __init_components__(self):
        self.divider = "•"
        self.store = cp.Subtitle(
            f"{self.page.client_storage.get('store_initials')} {self.divider} {self.page.client_storage.get('store_name')}"
        )
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
        self.controls = [self.store_section(), self.members_section()]

    def __init_config__(self):
        self.padding = 0
        self.expand = True
        self.floating_action_button = cp.HomeBtn()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def store_section(self) -> cp.Section:
        return cp.Section(
            "Store",
            cp.CenteredRow(
                [
                    self.store,
                    cp.IconBtn(
                        "edit_rounded",
                        tooltip="Edit Store",
                        on_click=self.edit_store,
                    ),
                ]
            ),
        )

    def members_section(self) -> cp.Section:
        db = Database()
        new_member_row = cp.CenteredRow(
            [
                self.new_name,
                self.new_initials,
                self.new_color,
                cp.PrimaryBtn("Add", on_click=self.add_member),
            ]
        )
        table_members = (
            cp.Subtitle("First add a member")
            if len(db.members) == 0
            else cp.Subtitle("YES")
        )
        return cp.Section(
            "Members",
            cp.CenteredColumn([new_member_row, table_members]),
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
