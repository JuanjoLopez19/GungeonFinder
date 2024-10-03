import os

from app.sites.Guns import GunsScrapper
from app.sites.items import ItemScrapper
from app.sites.Shrines import ShrinesScrapper
from app.sites.Synergies import SynergiesScrapper

ROOT_URL = "https://enterthegungeon.fandom.com/wiki/{}"

itemsScrapper = ItemScrapper(ROOT_URL.format("Items"))
shrinesScrapper = ShrinesScrapper(ROOT_URL.format("Shrines"))
gunsScrapper = GunsScrapper(ROOT_URL.format("Guns"))
synergiesScrapper = SynergiesScrapper(ROOT_URL.format("Synergies"))


elastic_config = {
    "host": os.getenv("ELASTIC_HOST"),
    "port": os.getenv("ELASTIC_PORT"),
    "user": os.getenv("ELASTIC_USER"),
    "password": os.getenv("ELASTIC_PASSWORD"),
}
