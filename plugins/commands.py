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

from discord.ext import commands
from tinydb import TinyDB, Query
from snowflake import f3

db = TinyDB('serverlinker.json')


class Linkage:
    """Commands to manage linkage"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="<server_id> <channel_id>")
    @commands.has_permissions(administrator=True)
    async def request(self, ctx, server_id: int, channel_id: int):
        """Request a link between the channel is command is run in and the target channel"""
        # Validate the inputs
        server = self.bot.get_guild(server_id)
        if not server:
            return await ctx.send("Sorry, I don't seem to be in a server with that ID")
        channel = server.get_channel(channel_id)
        if not channel:
            return await ctx.send("Sorry, there doesn't seem to be a channel with that ID in that server.")
        link_id = next(f3)
        db.insert({
            'id': link_id,
            'dest_server_id': server_id,
            'dest_channel_id': channel_id,
            'origin_server_id': ctx.guild.id,
            'origin_channel_id': ctx.channel.id,
            'active': False
        })

        return await ctx.send("Link request created successfully, an admin on the linked server can accept the"
                              f"request by running `$accept {link_id}`")

    @commands.command(usage="<link_id>")
    @commands.has_permissions(administrator=True)
    async def accept(self, ctx, request_id: int):
        """Accept an incoming link request"""
        link_query = Query()
        link = db.search(link_query.id == request_id)
        if len(link) < 1:
            return await ctx.send("Sorry, no request found with that ID")

        if not link[0]['dest_server_id'] == ctx.guild.id:
            return await ctx.send("Sorry, request is not for this guild")

        db.update({'active': True}, link_query.id == request_id)

        return await ctx.send("Yay! The channels are now linked! Messages will be synchronized between them.")

    @commands.command(usage="<link_id>")
    @commands.has_permissions(administrator=True)
    async def deny(self, ctx, request_id: int):
        """Deny an incoming link requests"""
        link_query = Query()
        link = db.search(link_query.id == request_id)
        if len(link) < 1:
            return await ctx.send("Sorry, no request found with that ID")

        if not link[0]['server_id'] == ctx.guild.id:
            return await ctx.send("Sorry, request is not for this guild")

        db.remove(link_query.id == request_id)

        return await ctx.send("Request has been denied.")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def list_requests(self, ctx):
        """List all incoming requests on this server"""
        link_query = Query()
        link = db.search(link_query.dest_server_id == ctx.guild.id)

        link_string = "**Current incoming link requests**\n\t"
        link_lines = []
        for l in link:
            server_name = ctx.bot.get_guild(l['origin_server_id']).name
            channel_name = ctx.guild.get_channel(l['dest_channel_id']).name
            link_lines.append(f"{l['id']}: From: {server_name}, To: #{channel_name}")
        return await ctx.send(link_string + '\n\t'.join(link_lines))


def setup(bot):
    bot.add_cog(Linkage(bot))
