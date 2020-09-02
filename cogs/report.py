import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def report(self, ctx, *, msg):
        await ctx.message.delete()

        channel = self.client.get_channel(741011181484900464)
        staff = discord.utils.get(ctx.guild.roles, id=749953613773930497)

        embed = discord.Embed(colour=discord.Colour.from_rgb(255,255,0))

        embed.add_field(name=f'__**Report:**__', value=f"<@{ctx.author.id}> Reported:", inline=False)
        embed.add_field(name=msg, value="­")
        embed.set_footer(text=f"ID: {ctx.message.author.id}")

        await channel.send(staff.mention, embed=embed)
        await ctx.author.send("Your report has been sent successfully! Action will be taken accordingly.")


def setup(client):
    client.add_cog(AdminCommands(client))