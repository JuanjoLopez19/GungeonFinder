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

- Run the following command on the `wsl command shell` to start the application:

```bash
docker compose up -d --build
```
### When deplying the two images at the sametime take in count that the elasticsearch service take a few time to initialize, maybe the GUI will show an error, just wait a few seconds and restart the GUI service to make the connection succesfully

## The docker image can be found in my docker hub [page](https://hub.docker.com/r/juanjolopez19/gungeon-finder)
Developed by @JuanjoLopez19
