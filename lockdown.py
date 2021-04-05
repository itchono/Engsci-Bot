import discord
from discord.ext import commands, tasks

from utils.logger import logger
from utils.utilities import local_time
import cogs

import datetime
import pytz
import re

from config import cfg

'''
Format:
[name]: %Y-%m-%d %H:%M (start/end)
'''


# These channels are not touched during lockdown
EXCLUSIONS = ["admin",
              "mods",
              "mod-logs",
              "mod-voice",
              "announcements",
              "to-do-list",
              "scheduled-lockdowns"]

# Scheduled Lockdowns channel
CHANNEL_ID = 796831543498637342


def included_channels(guild) -> list:
    '''
    Channels in which we need to lock down
    '''

    lockers = guild.channels[:]

    # Filter out channels with special permission sets

    for channel in guild.channels:

        if channel.name in EXCLUSIONS:
            lockers.remove(channel)
            logger.warn(
                f"Lockdown: Skipping Channel {channel} Reason: In exclusion list")
            continue
            

        for overwrite in channel.overwrites:
            # overwrites is a dictionary btw
            if isinstance(overwrite, discord.Role) \
                and str(overwrite) not in [
                    "2T4", "@everyone", "New Member"]:
                lockers.remove(channel)

                logger.warn(
                    f"Lockdown: Skipping Channel {channel} Reason: Extra permissions detected")
                break
    return lockers


def parse_lockdown(content: str) -> tuple:
    try:
        pattern = r"^\[(.*?)\]: (.*?) \((.*?)\)$"

        name, dtstr, action = re.match(pattern, content).groups()

        t = datetime.datetime.strptime(dtstr, "%Y-%m-%d %H:%M")
        t = pytz.timezone(cfg["Settings"]["timezone"]).localize(t)

        return t, action
    except Exception:
        return None


class Lockdown(commands.Cog):
    '''
    Locks down the server
    '''

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.process_lockdowns.start()

    def cog_unload(self):
        self.process_lockdowns.cancel()

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Moderator")
    async def lockdown(self, ctx: commands.Context):
        '''
        Locks down the server
        '''
        await ctx.trigger_typing()

        for channel in included_channels(ctx.guild):
            await channel.set_permissions(
                ctx.guild.default_role, read_messages=False)

        # Special Cases
        weeklygame = discord.utils.get(
            ctx.guild.text_channels,
            name="weekly-game-nights🎲")
        await weeklygame.set_permissions(discord.utils.get(ctx.guild.roles, name="Weekly Gamer"), read_messages=False)
        weeklygame2 = discord.utils.get(
            ctx.guild.voice_channels, name="gamer-gang")
        await weeklygame2.set_permissions(discord.utils.get(ctx.guild.roles, name="Weekly Gamer"), read_messages=False)

        verified = discord.utils.get(
            ctx.guild.text_channels,
            name="verified-engsci✅")
        await verified.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), read_messages=False)
        verified2 = discord.utils.get(
            ctx.guild.voice_channels, name="Verified")
        await verified2.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), read_messages=False)

        for cog in cogs.lockdown_cogs:
            try:
                self.bot.remove_cog(cog.__name__)
            except Exception:
                logger.exception("Removing cogs")

        if not ctx.channel.id == CHANNEL_ID:
            await ctx.send("LOCKDOWN INITIATED")

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Moderator")
    async def unlockdown(self, ctx: commands.Context):
        '''
        Unlocks the server
        '''
        await ctx.trigger_typing()

        for channel in included_channels(ctx.guild):
            await channel.set_permissions(ctx.guild.default_role, read_messages=None)

        # Special Cases
        weeklygame = discord.utils.get(
            ctx.guild.text_channels,
            name="weekly-game-nights🎲")
        await weeklygame.set_permissions(discord.utils.get(ctx.guild.roles, name="Weekly Gamer"), read_messages=True)
        weeklygame2 = discord.utils.get(
            ctx.guild.voice_channels, name="gamer-gang")
        await weeklygame2.set_permissions(discord.utils.get(ctx.guild.roles, name="Weekly Gamer"), read_messages=True)

        verified = discord.utils.get(
            ctx.guild.text_channels,
            name="verified-engsci✅")
        await verified.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), read_messages=True)
        verified2 = discord.utils.get(
            ctx.guild.voice_channels, name="Verified")
        await verified2.set_permissions(discord.utils.get(ctx.guild.roles, name="Verified"), read_messages=True)

        library = discord.utils.get(ctx.guild.voice_channels, id=808470402288189521)
        await library.set_permissions(ctx.guild.default_role, speak=False)

        for cog in cogs.lockdown_cogs:
            try:
                self.bot.add_cog(cog(self.bot))
            except Exception:
                logger.exception("Loading cogs")

        try:
            if not ctx.channel.id == CHANNEL_ID:
                await ctx.send("LOCKDOWN RELEASED")
            else:
                general = discord.utils.get(ctx.guild.text_channels, name="general")
                await general.send("Lockdown released. Please follow any additional guidelines about discussing the test in the meantime.\nPRO TIP: Press `Shift-Esc` to mark all of your channels as read")
        except Exception:
                logger.exception("announcement")

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Moderator")
    async def schedule(self, ctx: commands.Context,
                       name: str, date:str, time:str, duration: float):
        '''
        Schedules a lockdown to be run
        Duration in minutes
        '''
        channel = self.bot.get_channel(CHANNEL_ID)

        t = datetime.datetime.strptime(
            date + " " + time, "%Y-%m-%d %H:%M")
        tz_corrected = pytz.timezone(cfg["Settings"]["timezone"]).localize(t)

        delta = datetime.timedelta(minutes=duration)

        tz_corrected_end = tz_corrected + delta

        await channel.send(
            f"[{name}]: {tz_corrected.strftime('%Y-%m-%d %H:%M')} (start)")

        await channel.send(
            f"[{name}]: {tz_corrected_end.strftime('%Y-%m-%d %H:%M')} (end)")

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            channel = self.bot.get_channel(CHANNEL_ID)

            logger.info("LOCKDOWN: Found channel.")

            num_lockdowns = 0

            async for msg in channel.history():
                assert msg.author == self.bot.user

                if parse_lockdown(msg.content):
                    num_lockdowns += 1

            logger.info(
                f"LOCKDOWN: All messages are clean. {num_lockdowns} lockdown events scheduled.")
        except Exception:
            logger.critical("LOCKDOWN: Channel is not found or not clean.")

    @tasks.loop(seconds=1.0)
    async def process_lockdowns(self):
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(CHANNEL_ID)
        async for msg in channel.history(oldest_first=True):

            parsed = parse_lockdown(msg.content)

            if parsed is not None:
                t, action = parsed

                if t < local_time():

                    logger.info(action)

                    ctx = await self.bot.get_context(msg)

                    if action == "start":
                        await self.lockdown(ctx)
                    elif action == "end":
                        await self.unlockdown(ctx)

                    await msg.edit(content=f"✅ {msg.content}")
                break
