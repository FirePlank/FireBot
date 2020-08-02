import discord
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['mimic', 'paste', 'say'])
    async def echo(self, ctx, *, sentence):
        await ctx.send(sentence)


def setup(client):
    client.add_cog(Fun(client))