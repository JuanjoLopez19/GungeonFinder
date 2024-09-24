from io import BytesIO
import json

import requests
import wx
import os

from wx.core import CommandEvent
from src import client


class GungeonFinderApp(wx.Frame):
    def __init__(self, parent, title):
        super(GungeonFinderApp, self).__init__(parent, title=title, size=(700, 450))
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

    # TODO manage the tooltip and format the data in a better way
    def on_listbox_click(self, event: CommandEvent):
        handler = {
            "gun": lambda x: {
                "name": x["name"],
                "description": x["notes"],
                "quality": x["quality"],
                "gun_type": x["type"],
                "dps": x["dps"],
                "magazine_size": x["magazine_size"],
                "ammo_capacity": x["ammo_capacity"],
                "damage": x["damage"],
            },
            "item": lambda x: {
                "name": x["name"],
                "description": x["description"],
                "utility": x["utility"],
                "quality": x["quality"],
                "effect": x["effect"],
            },
            "shrine": lambda x: {
                "name": x["name"],
                "description": x["description"],
                "effect": x["effect"],
            },
            "synergy": lambda x: {
                "name": x["name"],
                "description": x["effect"],
                "items": x["synergy"],
            },
        }
        selection = event.GetIndex()
        item = self.list_ctrl.GetItemText(selection, 1)
        res = client.search(item)[0]

        tooltip_text = json.dumps(handler[res["type"]](res))

        wx.TipWindow(self.list_ctrl, tooltip_text, maxLength=500)

        event.Skip()

    def on_resize(self, event):
        width = self.list_ctrl.GetClientSize().width
        num_columns = self.list_ctrl.GetColumnCount()
        if num_columns > 0:
            for col in range(num_columns):
                self.list_ctrl.SetColumnWidth(col, width // num_columns)
        event.Skip()
