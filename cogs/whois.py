import discord
from discord.ext import commands
from datetime import datetime


class HelpfulCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def whois(self, ctx, *, members=None):
        mentions = ctx.message.mentions
        if len(mentions) == 0:
            image_url = ctx.author.avatar_url
            author_name = ctx.author.name
            author = ctx.author
            joined_at = ctx.author.joined_at
            nick = ctx.author.nick
            status = ctx.author.status
            activity = ctx.author.activity
            id = ctx.author.id
            created_at = ctx.author.created_at
        else:
            image_url = mentions[0].avatar_url
            author_name = mentions[0].name
            author = mentions[0]
            joined_at = mentions[0].joined_at
            nick = mentions[0].nick
            status = mentions[0].status
            activity = mentions[0].activity
            id = mentions[0].id
            created_at = mentions[0].created_at

        joined_at = joined_at.strftime("%d-%m-%Y")
        created_at = created_at.strftime("%d-%m-%Y")

        message = discord.Embed(title=author_name, color=discord.Colour.orange())
        message.add_field(name="ID", value=id, inline=True)
        message.add_field(name="Account created at", value=created_at, inline=True)
        message.add_field(name="Nickname", value=nick, inline=True)
        message.add_field(name="Joined at", value=joined_at, inline=True)
        message.add_field(name="Status", value=status, inline=True)
        message.add_field(name="Activity", value=activity, inline=True)
        message.set_author(name=author, icon_url=image_url)

        await ctx.send(embed=message)


def setup(client):
    client.add_cog(HelpfulCommands(client))