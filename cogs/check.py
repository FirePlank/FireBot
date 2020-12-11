import discord
from discord.ext import commands
from datetime import datetime, timedelta


class Helpful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["stats", "activity", "messages"])
    async def check(self, ctx, timeframe=7, channel: discord.TextChannel = None, *, user: discord.Member = None):
        if timeframe > 1968:
            await ctx.channel.send("Sorry. The maximum of days you can check is 1968.")
        elif timeframe <= 0:
            await ctx.channel.send("Sorry. The minimum of days you can check is one.")

        else:
            if not channel:
                channel = ctx.channel
            if not user:
                user = ctx.author

            async with ctx.channel.typing():
                msg = await ctx.channel.send('Calculating...')
                await msg.add_reaction('🔎')

                counter = 0
                async for message in channel.history(limit=5000, after=datetime.today() - timedelta(days=timeframe)):
                    if message.author.id == user.id:
                        counter += 1

                await msg.remove_reaction('🔎', member=message.author)

                if counter >= 5000:
                    await msg.edit(content=f'{user} has sent over 5000 messages in the channel "{channel}" within the last {timeframe} days!')
                else:
                    await msg.edit(content=f'{user} has sent {str(counter)} messages in the channel "{channel}" within the last {timeframe} days.')


def setup(client):
    client.add_cog(Helpful(client))
