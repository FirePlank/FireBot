import discord
from discord.ext import commands
from datetime import datetime


class HelpfulCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def whois(self, ctx, user: discord.Member = None):
        if not user:user=ctx.author
        image_url = user.avatar_url
        author = user
        joined_at = user.joined_at
        nick = user.nick
        status = user.status
        activity = user.activity
        created_at = user.created_at

        joined_at = joined_at.strftime("%d-%m-%Y")
        created_at = created_at.strftime("%d-%m-%Y")

        message = discord.Embed(color=discord.Colour.orange())
        message.add_field(name="Account created at", value=created_at, inline=False)
        message.add_field(name="Joined at", value=joined_at, inline=False)
        message.add_field(name="Nickname", value=nick, inline=False)
        message.add_field(name="Status", value=status, inline=False)
        message.add_field(name="Activity", value=activity, inline=False)
        message.set_author(name=author, icon_url=image_url)

        await ctx.send(embed=message)


def setup(client):
    client.add_cog(HelpfulCommands(client))