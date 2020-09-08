import discord
from discord.ext import commands
import datetime

class Helpful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["suggestion"])
    async def poll(self, ctx, *, suggestion):
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name=f"Poll by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name=suggestion, value="­")
        embed.timestamp = datetime.datetime.utcnow()

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @commands.command()
    async def multi_choice(self, ctx, suggestion:str, *args):
        if len(args) > 10: await ctx.send("The maximum amount of choices you can pass is 10")
        await ctx.message.delete()
        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name=f"Poll by {ctx.author.name}", icon_url=ctx.author.avatar_url)
        embed.add_field(name=suggestion, value="­")
        embed.add_field(name="\n".join(args), value="­", inline=False)
        embed.timestamp = datetime.datetime.utcnow()

        msg = await ctx.send(embed=embed)
        for i in range(len(args)): await msg.add_reaction(reactions[i])


def setup(client):
    client.add_cog(Helpful(client))