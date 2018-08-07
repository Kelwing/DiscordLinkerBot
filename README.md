# Discord Server Linker
A simple bot that links channels together in a bi-directional fashion.

[![Docker Repository on Quay](https://quay.io/repository/kelwing/discordserverlinker/status "Docker Repository on Quay")](https://quay.io/repository/kelwing/discordserverlinker)
![GPL-3.0](https://img.shields.io/github/license/Kelwing/DiscordLinkerBot.svg)
[![Discord Server](https://img.shields.io/discord/194533269180514305.svg)](https://discord.gg/xmvACvn)

## Requirements
* Python 3.5 or 3.6
* Git

## Installation

### From Source
1. Check out the repository
2. `cd DiscordServerLinker`
3. `virtualenv -p python3.6 venv`
4. `source venv/bin/activate`
5. `pip install -r requirements.txt`
6. `export TOKEN=yourtokenhere`
7. `python main.py`

### Docker
1. `mkdir $HOME/link-data`
2. `docker run -e "TOKEN=yourtokenhere" -v $HOME/link-data:/opt/bot/data -d quay.io/kelwing/discordserverlinker`

## Support
If you need support or want to help with the project, contact Kelwing#0001 on Discord. 