from src.config import load
from src.sites.items import ItemScrapper
from src.sites.Shrines import ShrinesScrapper
from src.sites.Guns import GunsScrapper
from src.sites.Synergies import SynergiesScrapper
import os


def main():
    load()
    # items_list = ItemScrapper(os.getenv("ROOT_URL").format("Items")).get_data()
    # # ShrinesScrapper(os.getenv("ROOT_URL").format("Shrines")).get_data()
    # guns_list = GunsScrapper(os.getenv("ROOT_URL").format("Guns")).get_data()

    SynergiesScrapper(os.getenv("ROOT_URL").format("Synergies")).get_data()
