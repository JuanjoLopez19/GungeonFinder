import json
import os
import traceback
import webbrowser
from io import BytesIO

import requests
import wx
from wx.core import CommandEvent

from app import client

from app.ui.dialog import Modal


class GungeonFinderApp(wx.Frame):
    def __init__(self, parent, title):
        super(GungeonFinderApp, self).__init__(parent, title=title, size=(1200, 800))
        self.setToolbar()
        self.initialize_ui()
        self.set_custom_icon()
        self.image_dict = {}

    def set_custom_icon(self):
        """
        Sets a custom icon for the application window.

        This method fetches an icon from a specified URL, processes it, and sets it as the
        window icon. The icon is resized to 32x32 pixels with high quality.

        Raises:
            requests.exceptions.RequestException: If there is an issue with the HTTP request.
            wx._core.wxAssertionError: If there is an issue with setting the icon.
        """
        url = "https://static.wikia.nocookie.net/enterthegungeon_gamepedia/images/4/4a/Site-favicon.ico/revision/latest?cb=20210506213247"
        response = requests.get(url)
        icon_stream = BytesIO(response.content)
        icon = wx.Icon()
        icon.CopyFromBitmap(
            wx.Bitmap(wx.Image(icon_stream).Scale(32, 32, wx.IMAGE_QUALITY_HIGH))
        )
        self.SetIcon(icon)

    def setToolbar(self):
        """
        Sets up the toolbar with menu items for the application.
        This method creates a menu bar with an "Options" menu containing two items:
        - "Quit" (Ctrl+Q): Exits the application.
        - "Open Wiki" (Ctrl+O): Opens the wiki in a browser.
        If the corresponding image files exist in the specified paths, they are used as icons for the menu items.
        Binds the menu items to their respective event handlers:
        - `self.on_exit` for the "Quit" menu item.
        - `self.on_open_wiki` for the "Open Wiki" menu item.
        """
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()

        qmi = wx.MenuItem(file_menu, 1, "&Quit\tCtrl+Q")
        if os.path.exists(
            os.path.join(os.getcwd(), "app", "assets", "img", "quit.png")
        ):
            qmi.SetBitmap(
                wx.Bitmap(
                    wx.Image(
                        os.path.join(os.getcwd(), "app", "assets", "img", "quit.png")
                    ).Scale(12, 12, wx.IMAGE_QUALITY_HIGH)
                )
            )
        file_menu.Append(qmi)

        temp = wx.MenuItem(file_menu, 2, "&open Wiki\tCtrl+O")
        if os.path.exists(
            os.path.join(os.getcwd(), "app", "assets", "img", "browser.jpg")
        ):
            temp.SetBitmap(
                wx.Bitmap(
                    wx.Image(
                        os.path.join(os.getcwd(), "app", "assets", "img", "browser.jpg")
                    ).Scale(12, 12, wx.IMAGE_QUALITY_HIGH)
                )
            )
        file_menu.Append(temp)

        self.Bind(wx.EVT_MENU, self.on_exit, id=1)
        self.Bind(wx.EVT_MENU, self.on_open_wiki, id=2)

        menu_bar.Append(file_menu, "&Options")
        self.SetMenuBar(menu_bar)

    def initialize_ui(self):
        """
        Initializes the user interface for the application.
        This method sets up the main panel and layout for the UI, including the title and
        conditional UI elements based on the connection status to the ElasticSearch service.
        The UI components include:
        - A title label "Gungeon Finder".
        - An error message if the connection to ElasticSearch fails.
        - A search UI if the ElasticSearch data setup is successful.
        - An error message if there is an issue setting up the ElasticSearch data.
        The layout is managed using a vertical box sizer.
        Raises:
            ConnectionError: If there is an issue connecting to the ElasticSearch service.
            DataSetupError: If there is an issue setting up the ElasticSearch data.
        """
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
        panel.SetSizerAndFit(vbox)

    def render_image(self, image_path: str, panel: wx.Panel, is_local=False, *args):
        """
        Renders an image on a wx.Panel.

        Args:
            image_path (str): The path to the image file. Can be a local file path or a URL.
            panel (wx.Panel): The wx.Panel on which the image will be rendered.
            is_local (bool, optional): Flag indicating if the image is local. Defaults to False.
            *args: Variable length argument list. Expected to contain:
                - args[0] (int): The width to scale the image to.
                - args[1] (int): The height to scale the image to.
                - args[2] (bool, optional): Flag indicating if the image should be returned as a wx.Bitmap. Defaults to True.

        Returns:
            wx.Bitmap or wx.StaticBitmap: The rendered image as a wx.Bitmap or wx.StaticBitmap, depending on the context.
        """
        if is_local:
            image = wx.Image(image_path, wx.BITMAP_TYPE_ANY).Scale(
                args[0], args[1], wx.IMAGE_QUALITY_HIGH
            )
            self.not_found_image = {"image": image}
            try:
                if len(args) < 2 and not args[2]:
                    return wx.Bitmap(image)
            except Exception as e:
                print(traceback.format_exc())
        else:
            if image_path in self.image_dict:
                return self.image_dict[image_path].get("bitmap")
            else:
                response = requests.get(image_path)
                bytes_image = BytesIO(response.content)
                image = wx.Image(bytes_image, wx.BITMAP_TYPE_ANY).Scale(
                    args[0], args[1], wx.IMAGE_LIST_NORMAL
                )
                self.image_dict[image_path] = {
                    "bitmap": wx.Bitmap(image),
                    "image": image,
                }
                return wx.Bitmap(image)
        bitmap = wx.StaticBitmap(panel, wx.ID_ANY, wx.Bitmap(image))
        return bitmap

    def create_error_ui(self, panel: wx.Panel, vbox: wx.BoxSizer, msg: str):
        """
        Creates an error UI panel with an error message and an exit button.
        Args:
            panel (wx.Panel): The parent panel to which the error UI will be added.
            vbox (wx.BoxSizer): The vertical box sizer to which the error UI will be added.
            msg (str): The error message to be displayed.
        Returns:
            None
        """
        hbox = wx.BoxSizer(wx.VERTICAL)
        first_row = wx.BoxSizer(wx.HORIZONTAL)
        first_row.Add(
            self.render_image(
                os.path.join(os.getcwd(), "app", "assets", "img", "error.png"),
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
        """
        Creates the search user interface components within the given panel and sizer.
        Args:
            panel (wx.Panel): The panel to which the search UI components will be added.
            vbox (wx.BoxSizer): The vertical box sizer to which the search UI components will be added.
        Components:
            - A horizontal box sizer containing:
                - A static text prompt for searching an item.
                - A text control for entering the search query, which binds to the on_text_change event.
            - A list control for displaying search results with columns for Icon, Name, Description, and Type.
                - Binds to the on_listbox_click event.
                - Uses an image list for displaying icons.
        """
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

        self.image_list = wx.ImageList(25, 25, True)

        self.list_ctrl.SetImageList(self.image_list, wx.IMAGE_LIST_SMALL)

        vbox.Add(self.list_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

    def adjust_column_widths(self):
        """
        Adjusts the widths of all columns in the list control to fit the content.
        This method iterates through each column and row of the list control,
        calculates the required width to fit the text and any associated image,
        and sets the column width accordingly. An additional padding of 25 pixels
        is added to ensure proper spacing.
        The method uses the device context (DC) to measure the text width and
        considers the image width for the first column if an image is present.
        Note:
            This method assumes that the list control and image list are already
            initialized and populated with items and images respectively.
        """
        font = self.list_ctrl.GetFont()
        dc = wx.ClientDC(self.list_ctrl)
        dc.SetFont(font)

        for col in range(self.list_ctrl.GetColumnCount()):
            max_width = 0

            for row in range(self.list_ctrl.GetItemCount()):
                text = self.list_ctrl.GetItemText(row, col)
                text_width, _ = dc.GetTextExtent(text)

                img_width = 0
                if col == 0:
                    img_idx = self.list_ctrl.GetItem(row).GetImage()
                    if img_idx != -1:
                        img_width, _ = self.image_list.GetSize(img_idx)

                total_width = text_width + img_width + 25
                if total_width > max_width:
                    max_width = total_width

            self.list_ctrl.SetColumnWidth(col, max_width)

    def on_exit(self, event: CommandEvent):
        """
        Handles the exit event by closing the application window.

        Args:
            event (CommandEvent): The event object containing information about the exit command.
        """
        self.Close()

    def on_open_wiki(self, event: CommandEvent):
        """
        Event handler for opening the Enter the Gungeon Wiki in a web browser.

        Args:
            event (CommandEvent): The event that triggered this handler.
        """
        webbrowser.open("https://enterthegungeon.gamepedia.com/Enter_the_Gungeon_Wiki")
        event.Skip()

    def on_text_change(self, event: CommandEvent):
        """
        Event handler for text change in the entry widget.
        This method is triggered when the text in the entry widget changes. It clears the current items in the list control,
        searches for items based on the entry's value, and populates the list control with the search results.
        Args:
            event (CommandEvent): The event object containing information about the text change event.
        The method performs the following steps:
        1. Clears all items in the list control.
        2. Defines handlers for different item types ('gun', 'item', 'shrine', 'synergy') to format the search results.
        3. If the entry widget has a value, it performs a search using the client.search method.
        4. Iterates over the search results and formats each item using the appropriate handler.
        5. Adds the formatted item to the image list and inserts it into the list control.
        6. Adjusts the column widths of the list control.
        7. Skips the event to allow further processing.
        """
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
                    os.path.join(
                        os.getcwd(), "src", "app", "assets", "img", "not_found.png"
                    ),
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

        self.adjust_column_widths()

    def on_listbox_click(self, event: CommandEvent):
        """
        Handles the event when an item in the listbox is clicked.
        This method retrieves the selected item's details from the listbox,
        fetches additional information from the client based on the item type,
        and displays the information in a modal dialog.
        Args:
            event (CommandEvent): The event object containing information about the click event.
        The method performs the following steps:
        1. Retrieves the index of the selected item from the event.
        2. Extracts the item name and type from the listbox based on the selected index.
        3. Searches for the item details using the client based on the item name and type.
        4. Formats the item details using a handler specific to the item type.
        5. Creates and displays a modal dialog with the item details and icon.
        6. Destroys the dialog after it is closed.
        7. Calls event.Skip() to allow further event processing.
        """
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
        item_type = self.list_ctrl.GetItemText(selection, 3)
        res = client.search(item, ["name"], item_type)[0]
        item = handler[res["type"]](res)

        dialog = Modal(
            self,
            title=item.get("name"),
            selection=item,
            item_icon=(
                self.image_dict.get(item.get("icon"))
                if self.image_dict.get(item.get("icon"), None)
                else self.not_found_image
            ),
        )
        dialog.ShowModal()
        dialog.Destroy()

        event.Skip()
