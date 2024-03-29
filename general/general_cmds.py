import discord
from discord.ext import commands

import typing

from utils.utilities import (get_uptime, get_host, dm_channel,
                             local_time, utc_to_local_time, bot_prefix)


class General(commands.Cog):
    '''
    General purpose commands for checking on the status of the bot,
    and various utilites like fetching avatars.
    '''

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def status(self, ctx: commands.Context):
        '''
        Shows the current status of the bot
        '''
        await ctx.send(f"**Uptime**: {round(get_uptime(), 1)}s\n"
                       f"Currently Connected to **{len(self.bot.guilds)}** "
                       f"server(s)\n**Host**: {get_host()}\n"
                       f"**API Latency**: {round(self.bot.latency, 4)}s\n"
                       f"Running discord.py version {discord.__version__}")

    @commands.command()
    async def dm(self, ctx: commands.Context, user:
                 typing.Union[discord.Member, discord.User] = None,
                 *, message: str):
        '''
        Sends a direct message to a given user via the bot
        '''
        channel = await dm_channel(user)
        await channel.send(message)

    @commands.command()
    async def dateof(self, ctx: commands.Context, *, thing:
                     typing.Union[discord.TextChannel, discord.User,
                                  discord.VoiceChannel, discord.Message,
                                  discord.Role, discord.Guild]):
        '''
        Gets the creation time of basically any Discord object.
        '''
        await ctx.send(f"That was created on "
                       f"{utc_to_local_time(thing.created_at).strftime('%B %m %Y at %I:%M:%S %p %Z')}")

    @commands.command(aliases=["lastmsg", "staleness"])
    @commands.guild_only()
    async def lastmessage(self, ctx: commands.Context,
                          channel: discord.TextChannel):
        '''
        Checks when the last message was sent in a channel
        '''
        msg = (await channel.history(limit=1).flatten()).pop()

        t0 = utc_to_local_time(msg.created_at)
        difference = (local_time() - t0).days

        await ctx.send(f"Last message in {channel.mention} was sent on"
                       f" {t0.strftime('%B %m %Y at %I:%M:%S %p %Z')} by "
                       f"`{msg.author.display_name}` ({difference} days ago.)")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context):
        '''
        Gets information about the server.
        '''
        e = discord.Embed(colour=ctx.guild.roles[-1].colour)
        e.set_thumbnail(url=ctx.guild.icon_url)
        e.set_author(name=f"Information for {ctx.guild.name}",
                     icon_url=ctx.guild.icon_url)

        e.add_field(name="Time of Creation",
                    value=ctx.guild.created_at.strftime(
                        '%B %m %Y at %I:%M:%S %p %Z'),
                    inline=False)

        e.add_field(name="Text Channels",
                    value=len(ctx.guild.text_channels))
        e.add_field(name="Voice Channels",
                    value=len(ctx.guild.voice_channels))
        e.add_field(name="Channel Categories",
                    value=len(ctx.guild.categories))

        e.add_field(name="Total Members",
                    value=ctx.guild.member_count)
        e.add_field(name="Human Members",
                    value=len([i for i in ctx.guild.members if not i.bot]))

        e.add_field(name="Emojis",
                    value=len(ctx.guild.emojis))
        e.add_field(name="Roles",
                    value=len(ctx.guild.roles))

        e.add_field(name="Server Icon", value=f"[Link]({ctx.guild.icon_url})")
        e.add_field(name="Owner", value=ctx.guild.owner.mention)

        e.set_footer(text=f"ID: {ctx.guild.id}")
        await ctx.send(embed=e)

    @commands.command()
    async def avatar(self, ctx: commands.Context, *,
                     member: typing.Union[discord.Member,
                                          discord.User] = None):
        '''
        Displays the avatar of a target user, or yourself by default
        Made by Slyflare, PhtephenLuu
        '''
        if not member:
            member = ctx.author

        col = member.colour if isinstance(member, discord.Member) \
            else discord.Color.dark_blue()

        a = discord.Embed(color=col,
                          title=f"{member.display_name}'s Avatar",
                          url=str(member.avatar_url_as(static_format="png")))

        a.set_image(url=member.avatar_url)
        await ctx.send(embed=a)

    @commands.command()
    @commands.guild_only()
    async def emojis(self, ctx: commands.Context):
        '''
        Shows all emoji in the server
        '''
        emoji = "".join([str(e) for e in ctx.guild.emojis])
        await ctx.send(f"{ctx.guild.name} has "
                       f"{len(ctx.guild.emojis)} emojis:\n{emoji}")

    @commands.command()
    @commands.guild_only()
    async def clear(self, ctx: commands.Context):
        '''
        Clears bot commands and messages from bot in the last 100 messages
        '''
        def check(message):
            return (message.content and message.content.startswith(bot_prefix)) or \
                message.author == self.bot.user
        await ctx.channel.purge(check=check, bulk=True)

    @commands.command()
    async def getlog(self, ctx: commands.Context):
        '''
        Uploads psi-tama's log file for analysis
        '''
        with open("engsci.log", "rb") as f:
            await ctx.send(file=discord.File(f, filename="engsci_log.txt"))
