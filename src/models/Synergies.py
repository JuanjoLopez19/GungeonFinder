import bs4


class Synergies:
    def __init__(self, id: int, *data: bs4.element.Tag) -> None:
        self.id = id

        self.name = (
            data[0].text.strip().replace("\n", "")
            if data[0].text.strip().replace("\n", "") != ""
            else "N/A"
        )

        self.effect = (
            data[3].text.strip().replace("\n", "")
            if len(data) == 4
            else data[2].text.strip().replace("\n", "")
        )
        print(len(data))
        print(self)

    def __str__(self) -> str:
        return f"{self.name} - {self.effect}"
