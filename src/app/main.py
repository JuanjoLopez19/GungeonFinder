import traceback
import wx

from app.ui.root import GungeonFinderApp


def main():
    try:
        app = wx.App(useBestVisual=True)
        gui = GungeonFinderApp(None, title="Gungeon Finder")
        gui.Center()
        gui.Show()
        app.MainLoop()
    except Exception as e:
        print(traceback.format_exc())
