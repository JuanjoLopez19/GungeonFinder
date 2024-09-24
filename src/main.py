import wx

from src.ui.root import GungeonFinderApp


def main():
    app = wx.App(useBestVisual=True)
    gui = GungeonFinderApp(None, title="Gungeon Finder")
    gui.Center()
    gui.Show()
    app.MainLoop()
