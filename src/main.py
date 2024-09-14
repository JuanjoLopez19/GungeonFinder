from src.config import load
from src.sites.items import ItemScrapper
from src.sites.Shrines import ShrinesScrapper
import os


def main():
    load()
    # ItemScrapper(os.getenv("ROOT_URL").format("Items")).get_data()
    ShrinesScrapper(os.getenv("ROOT_URL").format("Shrines")).get_data()
