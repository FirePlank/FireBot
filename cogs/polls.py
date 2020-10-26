import discord
from discord.ext import commands
import datetime

class Helpful(commands.Cog):

    def __init__(self, client):
        self.client = client

    def reactions(self):
        return {
            1: '1️⃣',
            2: '2️⃣',
            3: '3️⃣',
            4: '4️⃣',
            5: '5️⃣',
            6: '6️⃣',
            7: '7️⃣',
            8: '8️⃣',
            9: '9️⃣',
            10: '🔟'
        }


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
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def multi_choice(self, ctx, desc: str, *choices):
        if len(choices) < 2:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("You have to have at least two choices")
        if len(choices) > 10:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("You can have a maximum of 10 choices")

        await ctx.message.delete()

        embed = discord.Embed(description=f"**{desc}**\n\n" + "\n\n".join(
            f"{str(self.reactions[i])}  {choice}" for i, choice in enumerate(choices, 1)),
                              timestamp=datetime.datetime.utcnow(), color=discord.colour.Color.orange())
        embed.set_footer(text=f"Poll by {str(ctx.author)}")
        msg = await ctx.send(embed=embed)
        for i in range(1, len(choices) + 1):
            await msg.add_reaction(self.reactions[i])


def setup(client):
    client.add_cog(Helpful(client))