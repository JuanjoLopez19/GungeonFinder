import bs4
from bs4 import ResultSet

from src.models.Synergies import Synergies
from src.models.Guns import Guns
from src.models.items import Items
from src.scrapper import AbstractScrapper


class SynergiesScrapper(AbstractScrapper):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        temp = self.get_url()
        if temp:
            self.parsed_data = temp.select("table.wikitable > tbody > tr")[1:]
        else:
            self.logger.error("Error parsing the website")

    def get_data(
        self,
    ):
        """
        Get data from the website
        """

        # Synergies(0, *tr[0].find_all("td"))
        items: list[Synergies] = []
        for i, tr in enumerate(self.parsed_data):
            try:
                items.append(
                    Synergies(i, *[td for td in tr.contents if td.name == "td"])
                )
            except ValueError as e:
                self.logger.error(e)

        # # [print(i) for i in items]
        # return items
