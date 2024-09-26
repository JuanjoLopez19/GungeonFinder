import wx


class Modal(wx.Dialog):
    def __init__(self, parent: wx.Frame, title: str, selection: dict[str, any]):
        super(Modal, self).__init__(parent, title=title, size=(400, 200))

        self.SetIcon(parent.GetIcon())
        vbox = wx.BoxSizer(wx.VERTICAL)

        handler = {
            "gun": self._print_guns_ui,
            "item": self._print_items_ui,
            "shrine": self._print_shrines_ui,
            "synergy": self._print_synergies_ui,
        }

        if selection.get("type") in handler.keys():
            handler[selection.get("type")](selection, vbox)
        else:
            self._render_error_ui(vbox)

        self.SetSizer(vbox)

    def _print_guns_ui(self, data: dict[str, any], vbox: wx.BoxSizer): ...

    def _print_items_ui(self, data: dict[str, any], vbox: wx.BoxSizer): ...

    def _print_shrines_ui(self, data: dict[str, any], vbox: wx.BoxSizer): ...

    def _print_synergies_ui(self, data: dict[str, any], vbox: wx.BoxSizer): ...

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
