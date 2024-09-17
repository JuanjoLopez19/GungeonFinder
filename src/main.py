import os

import elasticsearch.helpers as helpers
import wx

from src.models.Guns import Guns
from src.models.items import Items
from src.models.Shrines import Shrines
from src.models.Synergies import Synergies
from src.ui.root import GungeonFinderApp

from . import client, gunsScrapper, itemsScrapper, shrinesScrapper, synergiesScrapper


def main():

    # if client.test_connection():
    #     if client.list_indexes() == {}:
    #         client.create_index(
    #             Guns.parse_index().get("name"), Guns.parse_index().get("body")
    #         )
    #         client.create_index(
    #             Items.parse_index().get("name"), Items.parse_index().get("body")
    #         )
    #         client.create_index(
    #             Synergies.parse_index().get("name"), Synergies.parse_index().get("body")
    #         )
    #         client.create_index(
    #             Shrines.parse_index().get("name"), Shrines.parse_index().get("body")
    #         )

    #         itemsScrapper.get_data()
    #         client.bulk_insert(itemsScrapper.bulk_insert())

    #         gunsScrapper.get_data()
    #         client.bulk_insert(gunsScrapper.bulk_insert())

    #         shrinesScrapper.get_data()
    #         client.bulk_insert(shrinesScrapper.bulk_insert())

    #         synergiesScrapper.get_data()
    #         client.bulk_insert(synergiesScrapper.bulk_insert())

    #     print(client.search("gun"))

    # else:
    #     print("Connection to ElasticSearch failed.")
    #     return
    app = wx.App(useBestVisual=True)
    GungeonFinderApp(None, title="Gungeon Finder").Show()
    app.MainLoop()
