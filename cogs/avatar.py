import discord
from discord.ext import commands


class HelpfulCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["av", "pfp"])
    async def avatar(self, ctx, *, member: discord.Member = None):
        if not member:member=ctx.message.author

        message = discord.Embed(title=str(member), color=discord.Colour.orange())
        message.set_image(url=member.avatar_url)

        await ctx.send(embed=message)


def setup(client):
    client.add_cog(HelpfulCommands(client))