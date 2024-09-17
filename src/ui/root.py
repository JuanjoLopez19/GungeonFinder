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

    def initialize_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(panel, label="Gungeon Finder")
        title.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vbox.Add(title, flag=wx.EXPAND | wx.ALL, border=10)

        self.entry = wx.TextCtrl(panel)
        self.entry.Bind(wx.EVT_TEXT, self.on_text_change)
        vbox.Add(self.entry, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        self.result_list = wx.ListBox(panel)  # Un ListBox para mostrar los resultados
        vbox.Add(self.result_list, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        panel.SetSizer(vbox)

    def on_text_change(self, event):
        # Limpiar resultados anteriores
        self.result_list.Clear()

        # Consultar a Elasticsearch y actualizar el ListBox
        if self.entry.GetValue():  # Asegurarse de no hacer una consulta vacía
            res = client.search(
                self.entry.GetValue()
            )  # Suponiendo que esto devuelve una lista de diccionarios
            for hit in res:
                self.result_list.Append(
                    hit["name"]
                )  # Asumiendo que cada hit tiene un campo "name"

        event.Skip()  # Permitir que otros manejadores de eventos procesen el evento
