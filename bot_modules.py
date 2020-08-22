import discord
from discord.ext import commands
from cfg import *
import datetime, math, typing

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

        if not (main_ch := discord.utils.get(user.guild.channels, name='arrivals')):
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


def textToEmoji(s):
    '''
    Converts text to equivalent emoji
    '''
    lookupTable = {"a":u"\U0001F1E6","b":u"\U0001F1E7","c":u"\U0001F1E8","d":u"\U0001F1E9","e":u"\U0001F1EA","f":u"\U0001F1EB","g":u"\U0001F1EC","h":u"\U0001F1ED","i":u"\U0001F1EE","j":u"\U0001F1EF","k":u"\U0001F1F0","l":u"\U0001F1F1","m":u"\U0001F1F2","n":u"\U0001F1F3","o":u"\U0001F1F4","p":u"\U0001F1F5","q":u"\U0001F1F6","r":u"\U0001F1F7","s":u"\U0001F1F8","t":u"\U0001F1F9","u":u"\U0001F1FA","v":u"\U0001F1FB","w":u"\U0001F1FC","x":u"\U0001F1FD","y":u"\U0001F1FE","z":u"\U0001F1FF"}
    s = s.lower()

    newS = ''
    for c in s:
        if c in lookupTable:
            newS += lookupTable[c] + " "
        elif c in "0123456789":
            newS += {0:"0️⃣", 1:"1️⃣", 2:"2️⃣", 3:"3️⃣", 4:"4️⃣", 5:"5️⃣", 6:"6️⃣", 7:"7️⃣", 8:"8️⃣", 9:"9️⃣"}[int(c)]
        else:
            newS += c
    return newS

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self._last_member = None

    @commands.command()
    async def dateof(self, ctx: commands.Context,*, thing: typing.Union[discord.TextChannel, discord.User, discord.VoiceChannel, discord.Message]):
        '''
        Gets the creation time of a Channel, User, or Message.
        '''
        await ctx.send(f"{thing} was created on {thing.created_at.strftime('%B %m %Y at %I:%M:%S %p %Z')}")

    @commands.command()
    async def staleness(self, ctx: commands.Context, channel: discord.TextChannel):
        '''
        Checks when the last message was sent in a channel
        '''
        msg = (await channel.history(limit=1).flatten()).pop()

        t0 = msg.created_at
        difference = (datetime.datetime.now() - t0).days

        await ctx.send(f"Last message in {channel.mention} was sent on {t0.strftime('%B %m %Y at %I:%M:%S %p %Z')} by `{msg.author.display_name}` ({difference} days ago.)")

    @commands.command()
    async def moststale(self, ctx: commands.Context, limit:int = None):
        '''
        Returns the top n most stale channels (default: 15%)
        '''

        channels = {}

        await ctx.trigger_typing()

        for channel in ctx.guild.text_channels:
            try:
                msg = (await channel.history(limit=1).flatten()).pop()

                t0 = msg.created_at
                difference = (datetime.datetime.now() - t0).days

                channels[channel.mention] = difference
            except: pass # empty channel

        if not limit: limit = math.ceil(0.15*len(channels)) # 15% of top

        top = sorted([(channels[k], k) for k in channels], reverse=True)[:limit]

        await ctx.send(f"Top {limit} most stale channels:\n" + "\n".join([f"{top.index(i) + 1}. {i[1]} ({i[0]} days)" for i in top]))

    @commands.command()
    async def poll(self, ctx: commands.Context, prompt:str, *options):
        f'''
        Creates a poll.
        Specify a prompt, and then split options by spaces.

        ex. !poll "apples or bananas?" "apples are better" "bananas are the best!"
        '''

        if len(options) < 36:

            lines = "\n".join([f"{i+1}) {options[i]}" for i in range(len(options))])

            msg = await ctx.send(f"**__POLL__:\n{prompt}**\n{lines}\n\n {ctx.author.mention}, react to this post with :octagonal_sign: to stop the poll.")

            reacts = "123456789abcdefghijklmnopqrstuvwxyz"

            ## Apply reactions
            for i in range(len(options)): await msg.add_reaction(textToEmoji(reacts[i]))
            await msg.add_reaction("🛑")

            ## Await Responses
            def check(reaction, user): return user == ctx.author and reaction.emoji == "🛑"

            await self.bot.wait_for('reaction_add', check=check)

            e = discord.Embed(title=f"**__POLL RESULT__:\n{prompt}**")

            for i in range(len(options)):

                reaction = (await ctx.channel.fetch_message(msg.id)).reactions[i]

                users = [u.mention for u in await reaction.users().flatten() if u != self.bot.user]

                people = " ".join(users)

                e.add_field(name=f"{i+1}) {options[i]}: {len(users)}", value = people if people else "No one", inline=False)

            await ctx.send(embed=e)

        else: await ctx.send("Sorry, you can only choose up to 35 options at a time.")   
