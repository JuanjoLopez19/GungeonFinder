class Items:
    def __init__(self, id: int, *data) -> None:
        if len(data) != 6:
            raise ValueError("Data must have 6 elements")

        self.id = id
        self.icon = data[0].find("a").attrs["href"]
        self.name = data[1].find("a").text
        self.type = data[2].text
        self.description = data[3].text
        self.quality = [
            q.find("img").attrs["alt"].split(" ")[0] for q in data[4].find_all("a")
        ]
        self.effect = data[5].text

    def __str__(self) -> str:
        return f"{self.name} - {self.type} - {self.description} - {self.quality} - {self.effect}"

    def dump(self):
        return {
            "id": self.id,
            "icon": self.icon,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "quality": self.quality,
            "effect": self.effect,
        }