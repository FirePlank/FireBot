import discord
from discord.ext import commands


class AvatarCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def av(self, ctx, *, members=None):
        mentions = ctx.message.mentions
        if len(mentions) == 0:
            image_url = (ctx.author.avatar_url)
            author_name = ctx.author.name
            author = ctx.author
        else:
            image_url = (mentions[0].avatar_url)
            author_name = mentions[0].name
            author = mentions[0]

        message = discord.Embed(title=author_name, color=int('f59e42', 16))
        message.set_author(name=author, icon_url=image_url)
        message.set_image(url=image_url)

        await ctx.send(embed=message)

def setup(client):
    client.add_cog(AvatarCommands(client))