import wx


class Modal(wx.Dialog):
    def __init__(
        self,
        parent: wx.Frame,
        title: str,
        selection: dict[str, any],
        item_icon: dict[str, wx.Image | wx.Bitmap],
    ):
        super(Modal, self).__init__(parent, title=title, size=(400, 250))

        self.SetIcon(parent.GetIcon())
        vbox = wx.BoxSizer(wx.VERTICAL)

        handler = {
            "gun": self._print_guns_ui,
            "item": self._print_items_ui,
            "shrine": self._print_shrines_ui,
            "synergy": self._print_synergies_ui,
        }

        if selection.get("type") in handler.keys():
            handler[selection.get("type")](selection, item_icon.get("image"), vbox)
        else:
            self._render_error_ui(vbox)

        self.SetSizer(vbox)

    def _print_guns_ui(self, data: dict[str, any], item_icon, vbox: wx.BoxSizer): ...

    def _print_items_ui(self, data: dict[str, any], item_icon, vbox: wx.BoxSizer): ...

    def _print_shrines_ui(
        self, data: dict[str, any], item_icon: wx.Image, vbox: wx.BoxSizer
    ):
        print(data)
        h_box = wx.BoxSizer(wx.HORIZONTAL)

        shrine_image = item_icon.Scale(100, 100, wx.IMAGE_LIST_NORMAL)
        shrine_icon = wx.StaticBitmap(self, bitmap=wx.Bitmap(shrine_image))
        h_box.Add(shrine_icon, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        v_box = wx.BoxSizer(wx.VERTICAL)

        shrine_text = wx.StaticText(
            self,
            label=f"Shrine: {data.get('name')}",
        )
        v_box.Add(shrine_text, 0, wx.RIGHT)

        shrine_description = wx.StaticText(
            self,
            label=f"Description: {data.get('description')}",
        )
        v_box.Add(shrine_description, 0, wx.RIGHT)

        shrine_effect = wx.StaticText(
            self,
            label=f"Effect: {data.get('effect')}",
        )
        v_box.Add(shrine_effect, 1, wx.RIGHT)

        h_box.Add(v_box, 1, wx.CENTER | wx.ALL | wx.EXPAND)
        vbox.Add(h_box, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

    def _print_synergies_ui(
        self, data: dict[str, any], item_icon, vbox: wx.BoxSizer
    ): ...

    def _render_error_ui(self, vbox: wx.BoxSizer):
        error_text = wx.StaticText(
            self,
            label="Error: Invalid selection",
            style=wx.ALIGN_CENTER,
            size=(100, 100),
        )
        vbox.Add(error_text, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        ok_button = wx.Button(self, label="Close modal", size=(150, 25))
        ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        vbox.Add(ok_button, 0, wx.CENTER)

    def on_ok(self, event):
        self.Destroy()
