from src.models.items import Items
from src.scrapper import AbstractScrapper


class ItemScrapper(AbstractScrapper):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        temp = self.get_url()
        if temp:
            self.parsed_data = temp.find("table", class_="wikitable")
        else:
            self.logger.error("Error parsing the website")

    def get_data(self):
        """
        Get data from the website
        """
        tbody = self.parsed_data.find("tbody")
        tr = tbody.find_all("tr")[1:]

        items: list[Items] = []
        for i, item in enumerate(tr):
            try:
                items.append(Items(i, *item.find_all("td")))
            except ValueError as e:
                self.logger.error(e)

        self.items = items

    def bulk_insert(self):
        return [
            {"_index": Items.parse_index().get("name"), "_source": item.dump()}
            for item in self.items
        ]
