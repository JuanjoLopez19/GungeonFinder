from src.models.Shrines import Shrines
from src.scrapper import AbstractScrapper


class ShrinesScrapper(AbstractScrapper):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        temp = self.get_url()
        if temp:
            self.parsed_data = temp.select("table.wikitable > tbody > tr")[1:]
        else:
            self.logger.error("Error parsing the website")

    def get_data(self):
        """
        Get data from the website
        """

        items: list[Shrines] = []
        for i, item in enumerate(self.parsed_data):
            try:
                items.append(Shrines(i, *item.find_all("td")))
            except ValueError as e:
                self.logger.error(e)
