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

        if not (main_ch := discord.utils.get(user.guild.channels, name='arrival')):
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
    async def gamer(self, ctx:commands.Context):
        '''
        Assigns/unassigns the gamer role
        '''

        try: 
            u = self.guild.get_member(ctx.author.id)
        except:
            await ctx.send(f"This command only works for members of {self.guild}.")
            return

        roles = u.roles

        gamer_role = discord.utils.get(self.guild.roles, name="Weekly Gamer")

        if gamer_role in roles:
            roles.remove(gamer_role)
            await ctx.send(f"{ctx.author.mention}, you have been removed from `Weekly Gamer`")
        else:
            roles.append(gamer_role)
            await ctx.send(f"{ctx.author.mention}, you have been added to `Weekly Gamer`")

        await u.edit(roles=roles)
        await ctx.message.add_reaction("👍")

    @commands.group()
    async def LEC(self, ctx:commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('Please specify which section you want to join i.e. !LEC 101 or !LEC 102')

    @LEC.command(name="101")
    async def LEC101(self, ctx:commands.Context):

        try: 
            u = self.guild.get_member(ctx.author.id)
        except:
            await ctx.send(f"This command only works for members of {self.guild}.")
            return


        role101 = discord.utils.get(self.guild.roles, name="LEC0101")
        role102 = discord.utils.get(self.guild.roles, name="LEC0102")

        roles = u.roles

        if role101 in roles:
            roles.remove(role101)
            await ctx.send("You no longer have LEC0101.", delete_after=30)
        else:
            if role102 in roles: 
                roles.remove(role102)
                await ctx.send("You no longer have LEC0102.", delete_after=30)
            roles.append(role101)
            await ctx.send("You now have LEC0101.", delete_after=30)

        await u.edit(roles=roles)
        await ctx.message.add_reaction("👍")

    @LEC.command(name="102")
    async def LEC102(self, ctx:commands.Context):

        try: 
            u = self.guild.get_member(ctx.author.id)
        except:
            await ctx.send(f"This command only works for members of {self.guild}.")
            return


        role101 = discord.utils.get(self.guild.roles, name="LEC0101")
        role102 = discord.utils.get(self.guild.roles, name="LEC0102")

        roles = u.roles

        if role102 in roles:
            roles.remove(role102)
            await ctx.send("You no longer have LEC0102.", delete_after=30)
        else:
            if role101 in roles: 
                roles.remove(role101)
                await ctx.send("You no longer have LEC0101.", delete_after=30)
            roles.append(role102)
            await ctx.send("You now have LEC0102.", delete_after=30)

        await u.edit(roles=roles)
        await ctx.message.add_reaction("👍")
        

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
        def pronoun_role(role_name):
            '''
            Gets the pronoun role from the server, if it exists.
            '''
            return discord.utils.get(self.guild.roles, name=role_name)


        currently_existent_roles = {"he/him", "she/her", "they/them", "ze/zir", "ze/hir", "other"}

        try: 
            u = self.guild.get_member(ctx.author.id)
        except:
            await ctx.send(f"This command only works for members of {self.guild}.")
            return

        if pronouns in currently_existent_roles:
            roles = set(u.roles)
            roles -= set([pronoun_role(i) for i in currently_existent_roles]) # if they want to change pronouns
            roles.update({pronoun_role(pronouns)})
            roles = list(roles)
            await u.edit(roles=roles)
            await ctx.message.add_reaction("👍")
        else:
            s = "\n* ".join(currently_existent_roles)
            await ctx.send(f"Our currently available pronouns are\n* {s}. \nI was unable to find your requested pronouns from this set. Please let a mod know if you would like a custom role.")
        
    