import discord
from discord.ext import commands


class Helpful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["origin", "github", "firebot"])
    async def source(self, ctx):
        await ctx.send("Here's the github link for the FireBot: https://github.com/FirePlank/FireBot")

def setup(client):
    client.add_cog(Helpful(client))