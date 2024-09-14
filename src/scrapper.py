import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import logging


class AbstractScrapper(ABC):
    def __init__(self, url: str) -> None:
        self.url = url
        self.logger = logging.getLogger(__name__)
        self.setup_logger()

    def get_url(self):
        res = requests.get(self.url)
        if res.status_code == 200:
            return BeautifulSoup(res.text, "html.parser")
        else:
            self.logger.error(f"Error: {res.status_code}")
            return None

    def setup_logger(self):
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    @abstractmethod
    def get_data(self):
        pass
