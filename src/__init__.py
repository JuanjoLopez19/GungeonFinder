import os

from src.config import load
from src.services.elastic_service import Elastic
from src.sites.Guns import GunsScrapper
from src.sites.items import ItemScrapper
from src.sites.Shrines import ShrinesScrapper
from src.sites.Synergies import SynergiesScrapper

load()

client = Elastic()

itemsScrapper = ItemScrapper(os.getenv("ROOT_URL").format("Items"))
shrinesScrapper = ShrinesScrapper(os.getenv("ROOT_URL").format("Shrines"))
gunsScrapper = GunsScrapper(os.getenv("ROOT_URL").format("Guns"))
synergiesScrapper = SynergiesScrapper(os.getenv("ROOT_URL").format("Synergies"))
