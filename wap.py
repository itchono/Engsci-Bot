import discord
from discord.ext import commands

from random import choice


class WAP(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        '''
        Replies when a WAP trigger is said in chat
        '''
        if message.author == self.bot.user:
            return

        with open("static/WAP.txt", encoding="utf-8") as f:
            WAP = f.read().split("\n")

        with open("static/triggers.txt") as f:
            triggers = f.read().split("\n")


        content_lower: str = message.content.lower()

        for word in triggers:
            if word in content_lower:

                # Word is now our designated trigger;
                # fetch lines from WAP with the word in it

                candidate_lines = [line for line in WAP if word.lower() in line.lower()]
                line_to_pick = choice(candidate_lines)
                await message.channel.send(line_to_pick)

                return
