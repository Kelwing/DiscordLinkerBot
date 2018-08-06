import discord
import datetime as dt
import logging
from discord.ext import commands
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
