import bs4
from bs4 import ResultSet

from app.models.Synergies import Synergies
from app.models.Guns import Guns
from app.models.items import Items
from app.scrapper import AbstractScrapper


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

        self.items = items

    def bulk_insert(self):
        return [
            {"_index": Synergies.parse_index().get("name"), "_source": item.dump()}
            for item in self.items
        ]


if __name__ == "__main__":
    url = "https://enterthegungeon.gamepedia.com/Synergies"
    scrapper = SynergiesScrapper(url)
    scrapper.get_data()
