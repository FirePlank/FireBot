import discord
import datetime
from discord.ext import commands


class FunCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["member_count", "count"])
    async def members(self, ctx):
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name="Member Count", icon_url=self.client.user.avatar_url)
        embed.add_field(name="Current Member Count:", value=ctx.guild.member_count)
        embed.set_footer(text=ctx.guild, icon_url=ctx.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(FunCommands(client))