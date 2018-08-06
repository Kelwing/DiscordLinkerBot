"""
    DiscordServerLinker Bot
    Copyright (C) 2018  Kelwing#0001

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import discord
import logging
import os
from discord.ext import commands


logger = logging.getLogger('serverlinker')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

initial_extensions = [
    'plugins.commands',
    'plugins.handlers'
]

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('$'))


logger.info("""
  _________                               .____    .__        __                 
 /   _____/ ______________  __ ___________|    |   |__| ____ |  | __ ___________ 
 \_____  \_/ __ \_  __ \  \/ // __ \_  __ \    |   |  |/    \|  |/ // __ \_  __ \\
 /        \  ___/|  | \/\   /\  ___/|  | \/    |___|  |   |  \    <\  ___/|  | \/
/_______  /\___  >__|    \_/  \___  >__|  |_______ \__|___|  /__|_ \\\\___  >__|   
        \/     \/                 \/              \/       \/     \/    \/       
""")

logger.info("Created by Kelwing#0001")

if __name__ == '__main__':
    for ext in initial_extensions:
        try:
            logger.info(f"Loading {ext}...")
            bot.load_extension(ext)
        except Exception as e:
            logger.exception(f'Failed to load extension {ext}.')


@bot.event
async def on_ready():
    game = discord.Game(f"Type $help | auttaja.io "
                        f"| Serving {len(bot.guilds)} guilds on "
                        f"{bot.shard_count} shards")
    await bot.change_presence(activity=game)

    logger.info(f"{bot.user} is now online!")

bot.run(os.environ.get('TOKEN'), reconnect=True)
