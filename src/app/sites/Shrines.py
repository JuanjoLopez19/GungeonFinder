from app.models.Shrines import Shrines
from app.scrapper import AbstractScrapper


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

        self.items = items

    def bulk_insert(self):
        return [
            {"_index": Shrines.parse_index().get("name"), "_source": item.dump()}
            for item in self.items
        ]


if __name__ == "__main__":
    url = "https://enterthegungeon.gamepedia.com/Shrines"
    scrapper = ShrinesScrapper(url)
    scrapper.get_data()
