import json
import os
import webbrowser
from io import BytesIO

import requests
import wx
from wx.core import CommandEvent

from src import client

from src.ui.dialog import Modal


class GungeonFinderApp(wx.Frame):
    def __init__(self, parent, title):
        super(GungeonFinderApp, self).__init__(parent, title=title, size=(700, 450))
        self.setToolbar()
        self.initialize_ui()
        self.set_custom_icon()
        self.image_dict = {}

    def set_custom_icon(self):
        url = "https://static.wikia.nocookie.net/enterthegungeon_gamepedia/images/4/4a/Site-favicon.ico/revision/latest?cb=20210506213247"
        response = requests.get(url)
        icon_stream = BytesIO(response.content)
        icon = wx.Icon()
        icon.CopyFromBitmap(
            wx.Bitmap(wx.Image(icon_stream).Scale(32, 32, wx.IMAGE_QUALITY_HIGH))
        )
        self.SetIcon(icon)

    def setToolbar(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()

        qmi = wx.MenuItem(file_menu, 1, "&Quit\tCtrl+Q")
        qmi.SetBitmap(
            wx.Bitmap(
                wx.Image(
                    os.path.join(os.getcwd(), "src", "assets", "img", "quit.png")
                ).Scale(12, 12, wx.IMAGE_QUALITY_HIGH)
            )
        )
        file_menu.Append(qmi)

        temp = wx.MenuItem(file_menu, 2, "&open Wiki\tCtrl+O")
        temp.SetBitmap(
            wx.Bitmap(
                wx.Image(
                    os.path.join(os.getcwd(), "src", "assets", "img", "browser.jpg")
                ).Scale(12, 12, wx.IMAGE_QUALITY_HIGH)
            )
        )
        file_menu.Append(temp)

        self.Bind(wx.EVT_MENU, self.on_exit, id=1)
        self.Bind(wx.EVT_MENU, self.on_open_wiki, id=2)

        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)

    def initialize_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="Gungeon Finder")
        title.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(title, flag=wx.CENTER | wx.ALL, border=10)

        if not client.test_connection():
            self.create_error_ui(
                panel,
                vbox,
                "Connection error, please check out the ElasticSearch service and restart the application.",
            )

        else:
            if client._setup_elastic_data():
                self.create_search_ui(panel, vbox)
            else:
                self.create_error_ui(
                    panel,
                    vbox,
                    "There was an error while setting up the ElasticSearch data, please check the logs.",
                )
        panel.SetSizer(vbox)

    def render_image(self, image_path: str, panel: wx.Panel, is_local=False, *args):
        if is_local:
            image = wx.Image(image_path, wx.BITMAP_TYPE_ANY).Scale(
                args[0], args[1], wx.IMAGE_QUALITY_HIGH
            )
            try:
                if not args[2]:
                    return wx.Bitmap(image)
            except Exception as e:
                print(e)
        else:
            if image_path in self.image_dict:
                return self.image_dict[image_path]
            else:
                response = requests.get(image_path)
                bytes_image = BytesIO(response.content)
                image = wx.Image(bytes_image, wx.BITMAP_TYPE_ANY).Scale(
                    args[0], args[1], wx.IMAGE_LIST_NORMAL
                )
                self.image_dict[image_path] = wx.Bitmap(image)
                return wx.Bitmap(image)
        bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(image))
        return bitmap

    def create_error_ui(self, panel: wx.Panel, vbox: wx.BoxSizer, msg: str):
        hbox = wx.BoxSizer(wx.VERTICAL)
        first_row = wx.BoxSizer(wx.HORIZONTAL)
        first_row.Add(
            self.render_image(
                os.path.join(os.getcwd(), "src", "assets", "img", "error.png"),
                panel,
                True,
                *[50, 50],
            ),
            flag=wx.LEFT,
            border=8,
        )
        error = wx.StaticText(
            panel,
            label=msg,
        )
        first_row.Add(error, flag=wx.EXPAND | wx.ALL, border=15)

        hbox.Add(first_row, flag=wx.EXPAND | wx.ALL, border=20)

        second_row = wx.BoxSizer(wx.HORIZONTAL)
        exit_button = wx.Button(
            panel,
            label="Exit",
            size=(70, 30),
            id=wx.ID_EXIT,
            name="exit",
            style=wx.BORDER_SUNKEN,
        )
        exit_button.Bind(wx.EVT_BUTTON, lambda e: self.on_exit(e))
        second_row.Add(
            exit_button,
            proportion=1,
            flag=wx.CENTRE | wx.ALL,
            border=10,
        )
        hbox.Add(second_row, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=10)

    def create_search_ui(self, panel: wx.Panel, vbox: wx.BoxSizer):
        h_box = wx.BoxSizer(wx.HORIZONTAL)
        prompt = wx.StaticText(panel, label="Search for an item: ")
        h_box.Add(prompt, flag=wx.EXPAND | wx.ALL)

        self.entry = wx.TextCtrl(panel)
        self.entry.Bind(wx.EVT_TEXT, self.on_text_change)
        h_box.Add(self.entry, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT)
        vbox.Add(h_box, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.list_ctrl.InsertColumn(0, "Icon")
        self.list_ctrl.InsertColumn(1, "Name")
        self.list_ctrl.InsertColumn(2, "Description")
        self.list_ctrl.InsertColumn(3, "Type")

        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_listbox_click)
        self.list_ctrl.Bind(wx.EVT_SIZE, self.on_resize)

        self.image_list = wx.ImageList(25, 25, True)

        self.list_ctrl.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)

        vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

    def on_exit(self, event: CommandEvent):
        self.Close()

    def on_open_wiki(self, event: CommandEvent):
        print("Opening the wiki")

        webbrowser.open("https://enterthegungeon.gamepedia.com/Enter_the_Gungeon_Wiki")
        event.Skip()

    def on_text_change(self, event: CommandEvent):
        self.list_ctrl.DeleteAllItems()
        handler = {
            "gun": lambda x: {
                "icon": self.render_image(x["icon"], self.list_ctrl, False, *[25, 25]),
                "name": x["name"],
                "description": x["notes"],
                "type": x["type"],
            },
            "item": lambda x: {
                "icon": self.render_image(x["icon"], self.list_ctrl, False, *[25, 25]),
                "name": x["name"],
                "description": x["description"],
                "type": x["type"],
            },
            "shrine": lambda x: {
                "icon": self.render_image(x["icon"], self.list_ctrl, False, *[25, 25]),
                "name": x["name"],
                "description": x["description"],
                "type": x["type"],
            },
            "synergy": lambda x: {
                "icon": self.render_image(
                    os.path.join(os.getcwd(), "src", "assets", "img", "not_found.png"),
                    self.list_ctrl,
                    True,
                    *[25, 25, False],
                ),
                "name": x["name"],
                "description": x["effect"],
                "type": x["type"],
            },
        }
        if self.entry.GetValue():
            res = client.search(self.entry.GetValue())
            for hit in res:
                item = handler[hit["type"]](hit)
                index = self.image_list.Add(item["icon"])

                list_index = self.list_ctrl.InsertItem(
                    self.list_ctrl.GetItemCount(), index
                )
                self.list_ctrl.SetItem(list_index, 1, item["name"])
                self.list_ctrl.SetItem(list_index, 2, item["description"])
                self.list_ctrl.SetItem(list_index, 3, item["type"])

            event.Skip()

    def on_listbox_click(self, event: CommandEvent):
        handler = {
            "gun": lambda x: {
                "icon": x["icon"],
                "name": x["name"],
                "description": x["notes"],
                "quality": x["quality"],
                "gun_type": x["type"],
                "dps": x["dps"],
                "magazine_size": x["magazine_size"],
                "ammo_capacity": x["ammo_capacity"],
                "damage": x["damage"],
                "type": x["type"],
            },
            "item": lambda x: {
                "icon": x["icon"],
                "name": x["name"],
                "description": x["description"],
                "utility": x["utility"],
                "quality": x["quality"],
                "type": x["type"],
                "effect": x["effect"],
            },
            "shrine": lambda x: {
                "icon": x["icon"],
                "name": x["name"],
                "description": x["description"],
                "type": x["type"],
                "effect": x["effect"],
            },
            "synergy": lambda x: {
                "icon": "",
                "name": x["name"],
                "description": x["effect"],
                "type": x["type"],
                "items": x["synergy"],
            },
        }
        selection = event.GetIndex()
        item = self.list_ctrl.GetItemText(selection, 1)
        res = client.search(item)[0]

        item = handler[res["type"]](res)

        dialog = Modal(self, title=item.get("name"), selection=item)
        dialog.ShowModal()
        dialog.Destroy()

        event.Skip()

    def on_resize(self, event):
        width = self.list_ctrl.GetClientSize().width
        num_columns = self.list_ctrl.GetColumnCount()
        if num_columns > 0:
            for col in range(num_columns):
                self.list_ctrl.SetColumnWidth(col, width // num_columns)
        event.Skip()
