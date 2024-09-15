import bs4


class Guns:
    def __init__(self, id: int, *data: bs4.element.Tag, table_type: int) -> None:

        self.id = id
        self.name = data[1].text.strip().replace("\n", "")
        self.icon = data[0].find("a").attrs["href"]
        self.notes = data[2].text.strip().replace("\n", "")
        if table_type == 0:
            self.quality = [
                q.find("img").attrs["alt"].split(" ")[0] for q in data[4].find_all("a")
            ]
            self.gun_type = data[5].text.strip().replace("\n", "")
            self.dps = data[6].text.strip().replace("\n", "")
            self.magazine_size = data[7].text.strip().replace("\n", "")
            self.ammo_capacity = data[8].text.strip().replace("\n", "")
            self.damage = data[9].text.strip().replace("\n", "")
        else:
            self.quality = [
                q.find("img").attrs["alt"].split(" ")[0] for q in data[3].find_all("a")
            ]
            self.gun_type = data[4].text.strip().replace("\n", "")
            self.dps = data[5].text.strip().replace("\n", "")
            self.magazine_size = data[6].text.strip().replace("\n", "")
            self.ammo_capacity = data[7].text.strip().replace("\n", "")
            self.damage = data[8].text.strip().replace("\n", "")

    def __str__(self) -> str:
        return f"{self.name} - {self.icon} - {self.notes} - {self.quality} - {self.gun_type} - {self.dps} - {self.magazine_size} - {self.ammo_capacity} - {self.damage}"