import bs4
from bs4 import ResultSet

from src.models.Guns import Guns
from src.scrapper import AbstractScrapper


class GunsScrapper(AbstractScrapper):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        temp = self.get_url()
        if temp:
            self.parsed_data: ResultSet[bs4.element.Tag] = temp.find_all("table")
        else:
            self.logger.error("Error parsing the website")

    def get_data(self):
        """
        Get data from the website
        """

        items: list[Guns] = []
        for j, table in enumerate(self.parsed_data):
            for i, item in enumerate(table.find_all("tr")[1:]):
                try:
                    items.append(
                        Guns(
                            i,
                            table_type=j,
                            *item.find_all("td"),
                        )
                    )
                except ValueError as e:
                    self.logger.error(e)

        self.items = items

    def bulk_insert(self):
        return [
            {"_index": Guns.parse_index().get("name"), "_source": item.dump()}
            for item in self.items
        ]


if __name__ == "__main__":
    url = "https://enterthegungeon.gamepedia.com/Guns"
    scrapper = GunsScrapper(url)
    scrapper.get_data()
