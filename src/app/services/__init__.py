import os

from app.config import load
from app.sites.Guns import GunsScrapper
from app.sites.items import ItemScrapper
from app.sites.Shrines import ShrinesScrapper
from app.sites.Synergies import SynergiesScrapper

load()

itemsScrapper = ItemScrapper(os.getenv("ROOT_URL").format("Items"))
shrinesScrapper = ShrinesScrapper(os.getenv("ROOT_URL").format("Shrines"))
gunsScrapper = GunsScrapper(os.getenv("ROOT_URL").format("Guns"))
synergiesScrapper = SynergiesScrapper(os.getenv("ROOT_URL").format("Synergies"))


elastic_config = {
    "host": os.getenv("ELASTIC_HOST"),
    "port": os.getenv("ELASTIC_PORT"),
    "user": os.getenv("ELASTIC_USER"),
    "password": os.getenv("ELASTIC_PASSWORD"),
}
