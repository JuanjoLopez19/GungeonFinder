import bs4


class Synergies:
    def __init__(self, id: int, *data: bs4.element.Tag) -> None:
        self.id = id

        self.name = (
            data[0].text.strip().replace("\n", "")
            if data[0].text.strip().replace("\n", "") != ""
            else "N/A"
        )

        if len(data) == 3:
            self.__parse_data_length_3(data[1], data[2])
        elif len(data) == 4:
            if data[2].find("table"):
                self.__parse_data_length_4(data[1], data[2], data[3])
            else:
                self.__parse_data_length_3(data[1], data[2])
        elif len(data) == 5:
            self.__parse_data_length_4(data[1], data[2], data[3])

    def __str__(self) -> str:
        return f"{self.name} - {self.synergy} - {self.effect}"

    def __parse_data_length_3(self, synergy: bs4.element.Tag, effect: bs4.element.Tag):
        items = synergy.find("table").find_all("td")

        self.synergy = ", ".join(
            [item.text.strip().replace("\n", "") for item in items]
        )

        self.effect = effect.text.strip().replace("\n", "")

    def __parse_data_length_4(
        self,
        main_item: bs4.element.Tag,
        auxiliary_items: bs4.element.Tag,
        effect: bs4.element.Tag,
    ):
        main_item = main_item.text.strip().replace("\n", "")
        auxiliary_items = auxiliary_items.find_all("td")
        temp = [main_item]
        temp.extend([item.text.strip().replace("\n", "") for item in auxiliary_items])
        self.synergy = ", ".join(temp)
        self.effect = effect.text.strip().replace("\n", "")

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "synergy": self.synergy,
            "effect": self.effect,
            "type": "synergy",
        }

    @staticmethod
    def parse_index():
        return {
            "name": "synergies",
            "body": {
                "name": {"type": "search_as_you_type"},
                "effect": {"type": "search_as_you_type"},
                "type": {"type": "search_as_you_type"},
            },
        }
