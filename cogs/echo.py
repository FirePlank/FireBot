import discord
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['mimic', 'paste', 'say'])
    async def echo(self, ctx, *, sentence):
        if "@everyone" in sentence or "@here" in sentence:
            await ctx.send(f"I'm sorry {ctx.author.mention}, but I don't want to say those things.")
        else:
            await ctx.send(sentence)


def setup(client):
    client.add_cog(Fun(client))