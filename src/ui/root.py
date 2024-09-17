from io import BytesIO

import requests
import wx

from src import client


class GungeonFinderApp(wx.Frame):
    def __init__(self, parent, title):
        super(GungeonFinderApp, self).__init__(parent, title=title, size=(700, 450))

        self.initialize_ui()
        self.set_custom_icon()

    def set_custom_icon(self):
        url = "https://static.wikia.nocookie.net/enterthegungeon_gamepedia/images/4/4a/Site-favicon.ico/revision/latest?cb=20210506213247"
        response = requests.get(url)
        icon_stream = BytesIO(response.content)
        icon = wx.Icon()
        icon.CopyFromBitmap(
            wx.Bitmap(wx.Image(icon_stream).Scale(32, 32, wx.IMAGE_QUALITY_HIGH))
        )
        self.SetIcon(icon)

        wx.ICONIZE = icon

        self.SetIcon(icon)

    def initialize_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="Gungeon Finder")
        title.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(title, flag=wx.EXPAND | wx.ALL, border=10)

        self.entry = wx.TextCtrl(panel)
        self.entry.Bind(wx.EVT_TEXT, self.on_text_change)
        vbox.Add(self.entry, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        panel.SetSizer(vbox)

    def on_text_change(self, event):
        # Este método se llama cada vez que se introduce un carácter en el campo de entrada
        print("Texto cambiado:", self.entry.GetValue())
        event.Skip()  # Importante para no detener el flujo de eventos

        res = client.search(self.entry.GetValue())

        for hit in res:
            print(hit["name"])
