import discord
from discord.ext import commands

import os
import dotenv

from cfg import *

from self_ping import SelfPing, keep_alive
from bot_modules import Listener, RoleManager
from pruner import Pruner

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN") # this is the bot token

'''
If you want to self host this, make a file in the root folder caleld .env, and add the following line:
TOKEN = <your bot token here>
'''

client = commands.Bot(command_prefix=commands.when_mentioned_or(BOT_PREFIX), case_insensitive=True,
                      help_command=commands.MinimalHelpCommand(
                          no_category="Help Command"))

cogs = [SelfPing, Listener, RoleManager, Pruner]    
for c in cogs: client.add_cog(c(client)) 


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game("[$] haha, get it?"))
    print(f"{client.user} is online.")
keep_alive() # start internal server to keep bot loaded
client.run(TOKEN) # log into Discord