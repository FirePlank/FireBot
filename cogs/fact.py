import aiohttp
import json
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fact(self, ctx):
        fact = "Fun Fact:\n"

        async with aiohttp.ClientSession() as session:
            async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as r:
                fact += json.loads(await r.text())["text"]

        await ctx.send(fact)


def setup(client):
    client.add_cog(Fun(client))
