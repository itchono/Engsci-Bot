import discord
from discord.ext import commands


class Copier(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_role("Moderator")
    async def copy(self, ctx: commands.Context, source: discord.TextChannel, destination: discord.TextChannel):
        '''
        Exports channel texts to another channel
        '''
        await ctx.send(f"{ctx.author.mention}, you are about to start a transfer from {source.mention} to {destination.mention}. **THIS IS A POTENTIALLY DESTRUCTIVE ACTION**. Please type `confirm` with the next 60 seconds to continue.")

        def check(m):
            return m.content == 'confirm' and m.channel == ctx.channel and m.author == ctx.author

        try:
            await self.bot.wait_for('message', timeout=60.0, check=check)

            await ctx.send(f"Transfer from {source.mention} to {destination.mention} is in progress. This will take several minutes depending on the size of the channel.")

            webhook = None
            for wh in await destination.webhooks():
                if wh.name == "ChannelCopier":
                    webhook = wh
            if not webhook:
                webhook = await destination.create_webhook(name="ChannelCopier", avatar=None)

            async for message in source.history(limit=None, oldest_first=True):
                try:
                    m = await webhook.send(wait=True, content=message.content, username=message.author.display_name, avatar_url=message.author.avatar_url, embeds=message.embeds, files=[await a.to_file() for a in message.attachments])
                    for r in message.reactions:
                        await m.add_reaction(r)
                except BaseException:
                    await ctx.send(f"Error processing message: {message.jump_url}")

        except asyncio.TimeoutError:
            await ctx.send("Tranfer aborted.")
        else:
            await ctx.send(f"Transfer from {source.mention} to {destination.mention} completed successfully.")
