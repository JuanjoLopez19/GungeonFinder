# Gungeon Finder

## Description

This is a tool that retrieves the information from The Enter the Gungeon Wiki [link](https://enterthegungeon.gamepedia.com/Enter_the_Gungeon_Wiki) and improve the information search for the user.
The tools needs to be run by linux or wsl eventhough is dockerized.

The information displayed is about:

- Items
- Guns
- Shrines
- Items & Guns Synergies

There's a main view that displays a text input that will update the list at the botton with the search's results updating in real time each time a character is typed.

Could be see a more detailed view of the selected item by double clicking on a item's list element.

## Installation

- Install the linux subsystem for windows [link](https://learn.microsoft.com/en-us/windows/wsl/install)

- Install docker [link](https://docs.docker.com/desktop/wsl/)

- In the linux enviornment, download x11 server and activate it:

```bash
sudo apt install x11-xserver-utils
xhost +local:root
```

- Clone the repository:

```bash
git clone https://github.com/JuanjoLopez19/GungeonFinder
```

- Change credentials in the `docker/python/python.env` file

- Add a `.env` for the docker-compose file with the following content:

```bash
PROJECT_NAME=""
ELASTIC_PASSWORD=""
ELASTIC_PORT=""
```

- Run the following command to start the application:

```bash
docker compose up -d --build
```

Developed by @JuanjoLopez19
