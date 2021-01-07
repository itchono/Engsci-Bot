import discord
from discord.ext import commands

import datetime


class Pruner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def requiem(self, ctx: commands.Context, day: int = 30):
        '''
        Generates a list of users who have not talked in the past x days (default 30)
        '''
        threshold = datetime.datetime.now() - datetime.timedelta(day)

        members = set(ctx.guild.members)

        await ctx.send('Scanning all members. This will take a while')

        for channel in ctx.guild.text_channels:

            authors = set([i.author for i in await channel.history(limit=None, after=threshold).flatten() if i.type == discord.MessageType.default])
            members -= authors

        await ctx.send(f"{len(members)} members detected to have not posted in the past {day} days.")

        paginator = commands.Paginator()

        for m in members:
            paginator.add_line(f"{m}, {m.id}")

        for p in paginator.pages:
            await ctx.send(p)
