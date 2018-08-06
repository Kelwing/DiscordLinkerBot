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
import datetime as dt
import logging
from tinydb import TinyDB, Query

db = TinyDB('serverlinker.json')

logger = logging.getLogger('serverlinker')


class Handlers:
    """Commands to manage linkage"""
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        link_query = Query()
        links = db.search(link_query.origin_channel_id == message.channel.id)
        links2 = db.search(link_query.dest_channel_id == message.channel.id)

        for link in links:
            if link['active'] is False:
                continue
            guild = self.bot.get_guild(link['dest_server_id'])
            channel = guild.get_channel(link['dest_channel_id'])
            em = discord.Embed(
                description=message.clean_content,
                timestamp=dt.datetime.utcnow()
            )

            em.set_author(
                name=f"{message.author}",
                icon_url=message.author.avatar_url
            )
            await channel.send(embed=em)
        for link in links2:
            if link['active'] is False:
                continue
            guild = self.bot.get_guild(link['origin_server_id'])
            channel = guild.get_channel(link['origin_channel_id'])
            em = discord.Embed(
                description=message.clean_content,
                timestamp=dt.datetime.utcnow()
            )

            em.set_author(
                name=f"{message.author}",
                icon_url=message.author.avatar_url
            )
            await channel.send(embed=em)


def setup(bot):
    bot.add_cog(Handlers(bot))
