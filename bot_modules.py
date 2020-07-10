import discord
from discord.ext import commands
from cfg import *

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, user: discord.Member):
        '''
        When a member joins the server.
        '''
        # NOTE: this requires channels "rules", "introduce-yourself" and "general" to be present. if you change their names, you must update them here.
        # as a failsafe, these will default to the first channel in the server if nothing is found.

        if not (rule_ch := discord.utils.get(user.guild.channels, name='rules')):
            rule_ch = user.guild.channels[0]

        if not (introductions_ch := discord.utils.get(user.guild.channels, name='introduce-yourself')):
            introductions_ch = user.guild.channels[0]

        if not (main_ch := discord.utils.get(user.guild.channels, name='general')):
            main_ch = user.guild.channels[0]

        await main_ch.send(f"{user.mention}, Welcome to the EngSci 2T3 Server! Please head over to {rule_ch.mention} and read our rules, then introduce yourself in {introductions_ch.mention}")

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        if not (g := self.bot.get_guild(DEFAULT_GUILD_ID)):  g = self.bot.guilds[0]
        self.guild = g
        print(f"Role manager loaded for: {g}")

    @commands.command()
    async def pronouns(self, ctx:commands.Context,*, pronouns):
        '''
        Assigns a pronoun role to the user calling it.

        Currently Existent Pronoun Roles:
        * he/him
        * she/her
        * they/them
        * ze/zir
        * ze/hir
        * other

        Message the mods if you would like other roles! 
        '''
        currently_existent_roles = {"he/him", "she/her", "they/them", "ze/zir", "ze/hir", "other"}

        try: 
            u = self.guild.get_member(ctx.author.id)
        except:
            await ctx.send(f"This command only works for members of {self.guild}.")
            return

        if pronouns in currently_existent_roles:
            roles = set(u.roles)
            roles -= set([self.pronoun_role(i) for i in currently_existent_roles]) # if they want to change pronouns
            roles.update({self.pronoun_role(pronouns)})
            roles = list(roles)
            await u.edit(roles=roles)
            await ctx.message.add_reaction("👍")
        else:
            s = "\n* ".join(currently_existent_roles)
            await ctx.send(f"Our currently available pronouns are\n* {s}. \nI was unable to find your requested pronouns from this set. Please let a mod know if you would like a custom role.")
        
    def pronoun_role(self, role_name):
        '''
        Gets the pronoun role from the server, if it exists.
        '''
        return discord.utils.get(self.guild.roles, name=role_name)