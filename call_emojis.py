import discord
from discord.ext import commands


class Emojis(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def react(self, ctx: commands.context, emoji: discord.Emoji):
        '''
        Reacts to the above message with a given emoji (can be animated)
        '''
        m = (await ctx.channel.history(limit=2).flatten())[1]
        # Get most recent non-bot message
        await m.add_reaction(emoji)

    @commands.command()
    async def emoji(self, ctx: commands.context, emoji: discord.Emoji):
        '''
        Sends the emoji into the channel (can be animated)
        '''
        await ctx.send(emoji)
