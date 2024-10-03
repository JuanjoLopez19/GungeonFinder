from typing import Callable
import wx

splitter: Callable[[str], str] = lambda x: ".\n".join(
    [y.strip() for y in x.split(".")]
).strip()


class Modal(wx.Dialog):
    def __init__(
        self,
        parent: wx.Frame,
        title: str,
        selection: dict[str, any],
        item_icon: dict[str, wx.Image | wx.Bitmap],
    ):
        super(Modal, self).__init__(
            parent,
            title=title,
            size=(450, 250) if selection.get("type") == "item" else (600, 250),
        )

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

        self.SetSizerAndFit(vbox)

    def _print_guns_ui(
        self, data: dict[str, any], item_icon: wx.Image, vbox: wx.BoxSizer
    ):
        h_box = wx.BoxSizer(wx.HORIZONTAL)

        gun_image = item_icon.Scale(75, 75, wx.IMAGE_QUALITY_NORMAL)
        gun_icon = wx.StaticBitmap(self, bitmap=wx.Bitmap(gun_image))
        h_box.Add(gun_icon, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        v_box = wx.BoxSizer(wx.VERTICAL)

        gun_text = wx.StaticText(
            self,
            label=f"Gun: {data.get('name')} --- Type: {data.get('gun_type')}\nQuality: {'/'.join(data.get('quality'))}",
        )
        v_box.Add(gun_text, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        gun_statics = wx.StaticText(
            self,
            label=f"Damage: {data.get('damage')} --- DPS: {data.get('dps')}\nMagazine Size: {data.get('magazine_size')} --- Ammo Capacity: {data.get('ammo_capacity')} ",
        )

        v_box.Add(gun_statics, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        gun_notes = wx.StaticText(
            self,
            label=f"Notes:\n{splitter(data.get('description'))}",
        )
        v_box.Add(gun_notes, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        h_box.Add(v_box, 0, wx.CENTER | wx.ALL | wx.EXPAND)
        vbox.Add(h_box, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

    def _print_items_ui(
        self, data: dict[str, any], item_icon: wx.Image, vbox: wx.BoxSizer
    ):
        h_box = wx.BoxSizer(wx.HORIZONTAL)

        item_image = item_icon.Scale(75, 75, wx.IMAGE_QUALITY_NORMAL)
        item_icon = wx.StaticBitmap(self, bitmap=wx.Bitmap(item_image))
        h_box.Add(item_icon, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        v_box = wx.BoxSizer(wx.VERTICAL)

        item_text = wx.StaticText(
            self,
            label=f"Item: {data.get('name')} --- Quality: {'/'.join(data.get('quality'))}",
        )
        v_box.Add(item_text, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        item_description = wx.StaticText(
            self,
            label=f"Description: {data.get('description')}",
        )
        v_box.Add(item_description, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        item_utility = wx.StaticText(
            self,
            label=f"Utility: {data.get('utility')}",
        )
        v_box.Add(item_utility, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        item_effect = wx.StaticText(
            self,
            label=f"Effect:\n{splitter(data.get('effect'))}",
        )
        v_box.Add(item_effect, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        h_box.Add(v_box, 0, wx.CENTER | wx.ALL | wx.EXPAND)
        vbox.Add(h_box, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

    def _print_shrines_ui(
        self, data: dict[str, any], item_icon: wx.Image, vbox: wx.BoxSizer
    ):
        h_box = wx.BoxSizer(wx.HORIZONTAL)

        shrine_image = item_icon.Scale(75, 75, wx.IMAGE_QUALITY_NORMAL)
        shrine_icon = wx.StaticBitmap(self, bitmap=wx.Bitmap(shrine_image))
        h_box.Add(shrine_icon, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        v_box = wx.BoxSizer(wx.VERTICAL)

        shrine_text = wx.StaticText(
            self,
            label=f"Shrine: {data.get('name')}",
        )
        v_box.Add(shrine_text, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        shrine_description = wx.StaticText(
            self,
            label=f"Description: {data.get('description')}",
        )
        v_box.Add(shrine_description, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        shrine_effect = wx.StaticText(
            self,
            label=f"Effect:\n{splitter(data.get('effect'))}",
        )
        v_box.Add(shrine_effect, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        h_box.Add(v_box, 0, wx.CENTER | wx.ALL | wx.EXPAND)
        vbox.Add(h_box, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

    def _print_synergies_ui(self, data: dict[str, any], item_icon, vbox: wx.BoxSizer):
        h_box = wx.BoxSizer(wx.HORIZONTAL)

        synergy_image = item_icon.Scale(50, 50, wx.IMAGE_LIST_NORMAL)
        synergy_icon = wx.StaticBitmap(self, bitmap=wx.Bitmap(synergy_image))
        h_box.Add(synergy_icon, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=10)

        v_box = wx.BoxSizer(wx.VERTICAL)

        synergy_text = wx.StaticText(
            self,
            label=f"Synergy: {data.get('name')}",
        )
        v_box.Add(synergy_text, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        synergy_description = wx.StaticText(
            self,
            label=f"Description: {data.get('description')}",
        )
        v_box.Add(synergy_description, 0, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        synergy_items = wx.StaticText(
            self,
            label=f"Items: {data.get('items')}",
        )
        v_box.Add(synergy_items, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        h_box.Add(v_box, 1, wx.CENTER | wx.ALL | wx.EXPAND)
        vbox.Add(h_box, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

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
