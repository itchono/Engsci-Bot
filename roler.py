import discord
from discord.ext import commands

from utils.logger import logger

CHANNEL_ID = 753408177919492097

# Getting roles channel
ROLES = {"🚲": "New Member", "🎮": "Weekly Gamer",
        "✈": "Aero",
        "⚛": "Physics",
        "🤖": "Robo",
        "🦠": "Biomed",
        "💰": "MSF",
        "⚡": "ECE",
        "🌞": "Energy",
        "📊": "MI",
        "🌐": "Global Grover"}


class Roler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.key_message = None

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            async for msg in self.bot.get_channel(CHANNEL_ID).history():
                if msg.author == self.bot.user:
                    self.key_message = msg
                    logger.info("ROLER: Found message.")
        except Exception:
            logger.critical("ROLER: Message not found.")

    @commands.command(enabled=True)
    @commands.has_role("Moderator")
    async def init(self, ctx: commands.Context):
        '''
        Makes a post in the get-roles channel
        '''
        async for msg in self.bot.get_channel(CHANNEL_ID).history():
            await msg.delete()

        sandwich = "Get your roles by reacting to this message:"

        for i in ROLES:
            sandwich += f"\n{i}: `{ROLES[i]}`"

        sandwich += "\n(If you have a role, but haven't reacted to the message, you can click on the reaction twice to remove your role. i.e. New Members)"

        m = await self.bot.get_channel(CHANNEL_ID).send(sandwich)

        for i in ROLES:
            await m.add_reaction(i)

        self.key_message = m

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):

        member = self.bot.get_channel(
            CHANNEL_ID).guild.get_member(event.user_id)

        if member != self.bot.user and event.message_id == self.key_message.id:

            r = discord.utils.get(
                self.key_message.guild.roles, name=ROLES[str(event.emoji)])

            roles = member.roles

            if not (r in roles):
                roles.append(r)
                await member.edit(roles=roles)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, event):

        member = self.bot.get_channel(
            CHANNEL_ID).guild.get_member(event.user_id)

        if member != self.bot.user and event.message_id == self.key_message.id:

            r = discord.utils.get(
                self.key_message.guild.roles, name=ROLES[str(event.emoji)])

            roles = member.roles

            if r in roles:
                roles.remove(r)
                await member.edit(roles=roles)
