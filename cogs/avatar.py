import discord
from discord.ext import commands


class HelpfulCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def av(self, ctx, *, user: discord.Member = None):
        if not user:user=ctx.author

        message = discord.Embed(title=user, color=discord.Colour.orange())
        message.set_image(url=user.avatar_url)

        await ctx.send(embed=message)


def setup(client):
    client.add_cog(HelpfulCommands(client))