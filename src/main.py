import os

from src.config import load
from src.sites.Guns import GunsScrapper
from src.sites.items import ItemScrapper
from src.sites.Shrines import ShrinesScrapper
from src.sites.Synergies import SynergiesScrapper


def main():
    load()
    ItemScrapper(os.getenv("ROOT_URL").format("Items")).get_data()
    ShrinesScrapper(os.getenv("ROOT_URL").format("Shrines")).get_data()
    GunsScrapper(os.getenv("ROOT_URL").format("Guns")).get_data()
    SynergiesScrapper(os.getenv("ROOT_URL").format("Synergies")).get_data()
