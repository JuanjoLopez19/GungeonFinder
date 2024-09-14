import bs4


class Shrines:
    def __init__(self, id: int, *data: bs4.element.Tag) -> None:
        # if len(data) != 4:
        #     raise ValueError("Data must have 6 elements")

        self.id = id
        print(data)
        print(data[0].find("a"))

    def __str__(self) -> str:
        return f"{self.name} - {self.type} - {self.description} - {self.quality} - {self.effect}"

    def dump(self):
        return {}
