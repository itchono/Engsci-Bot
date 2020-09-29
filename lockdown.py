import discord
from discord.ext import commands
import asyncio

class Lockdown(commands.Cog):

    EXCEPTIONS = [""]


    def __init__(self, bot): self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Moderator")
    async def lockdown(self, ctx: commands.Context):
        '''
        Locks down the server
        '''

        nonlock = ""

        lockers = ctx.guild.channels[:]

        for c in ctx.guild.channels:
            for o in c.overwrites:
                # this is a dictionary btw
                if type(o) == discord.Role and not str(o) in ["2T4", "@everyone", "New Member"]:
                    nonlock += f"{c.mention}\n"
                    lockers.remove(c)
                    break

        for channel in lockers:
            await channel.set_permissions(ctx.guild.default_role, read_messages=False)

        ## Special Cases
        weeklygame = discord.utils.get(ctx.guild.text_channels, name="weekly-game-nights")
        await weeklygame.set_permissions(discord.utils.get(ctx.guild.roles, name="Weekly Gamer"), read_messages=False)


        verified = discord.utils.get(ctx.guild.text_channels, name="verified-engsci")
        await verified.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), read_messages=False)

        verified2 = discord.utils.get(ctx.guild.voice_channels, name="verified")
        await verified2.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), read_messages=False)

        await ctx.send("LOCKDOWN INITIATED")

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Moderator")
    async def unlockdown(self, ctx: commands.Context):
        '''
        Unlocks the server
        '''

        lockers = ctx.guild.channels[:]

        for c in ctx.guild.channels:
            for o in c.overwrites:
                # this is a dictionary btw
                if type(o) == discord.Role and not str(o) in ["2T4", "@everyone", "New Member"]:
                    lockers.remove(c)
                    break

        for channel in lockers:
            await channel.set_permissions(ctx.guild.default_role, read_messages=None)

        ## Special Cases
        weeklygame = discord.utils.get(ctx.guild.text_channels, name="weekly-game-nights")
        await weeklygame.set_permissions(discord.utils.get(ctx.guild.roles, name="Weekly Gamer"), read_messages=True)

        verified = discord.utils.get(ctx.guild.text_channels, name="verified-engsci")
        await verified.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), read_messages=True)
        
        verified2 = discord.utils.get(ctx.guild.voice_channels, name="verified")
        await verified2.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), read_messages=True)

        await ctx.send("LOCKDOWN RELEASED")