import bs4


class Shrines:
    def __init__(self, id: int, *data: bs4.element.Tag) -> None:
        if len(data) != 4:
            self.id = id
            self.name = data[0].text.strip().replace("\n", "")
            self.icon = data[0].find("a").attrs["href"]
            self.description = data[1].text.strip().replace("\n", "")
            self.effect = self._parse_effect(data[3])
        else:
            self.id = id
            self.name = data[0].text.strip().replace("\n", "")
            self.icon = data[0].find("a").attrs["href"]
            self.description = data[1].text.strip().replace("\n", "")
            self.effect = data[3].text.strip().replace("\n", "")

    def __str__(self) -> str:
        return f"{self.name} - {self.icon} - {self.description} - {self.effect}"

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "description": self.description,
            "effect": self.effect,
        }

    def _parse_effect(self, effect: bs4.element.Tag):
        tbody = effect.find("tbody")
        tr = tbody.find_all("tr")[1:]
        aux = []
        aux.append("Good effect - Bad effect")
        for effect in tr:
            temp = effect.find_all("td")
            if len(temp) == 1:
                aux.append("{}".format(temp[0].text.strip().replace("\n", "")))
            else:
                aux.append(
                    f"{temp[0].text.strip()}: {temp[1].text.strip()} - {temp[2].text.strip()}: {temp[3].text.strip()}"
                )
        return ", ".join(aux)

    @staticmethod
    def parse_index():
        return {
            "name": "shrines",
            "body": {
                "name": {"type": "search_as_you_type"},
                "description": {"type": "search_as_you_type"},
                "type": {"type": "keyword"},
            },
        }

    def dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "description": self.description,
            "effect": self.effect,
            "type": "shrine",
        }
