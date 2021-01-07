import discord
from discord.ext import commands

import os
import dotenv
import time

from utils.utilities import bot_prefix, set_start_time
from utils.logger import logger

from self_ping import keep_alive
import cogs

dotenv.load_dotenv()
set_start_time(time.perf_counter())

'''
If you want to self host this,
make a file in the root folder called .env, and add the following line:
TOKEN = <your bot token here>
'''

client = commands.Bot(command_prefix=commands.when_mentioned_or(bot_prefix), case_insensitive=True,
                      help_command=commands.MinimalHelpCommand(
                          no_category="Help Command"))

for c in cogs.lockdown_cogs + cogs.other_cogs:
    client.add_cog(c(client))


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game(f"[{bot_prefix}] haha, get it?"))
    logger.info(f"{client.user} is online.")

keep_alive()
# start internal server to keep bot loaded
client.run(os.getenv("TOKEN"))
