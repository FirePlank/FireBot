import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")
        await ctx.send(f"The module {extension} has been loaded successfully!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")
        await ctx.send(f"The module '{extension}' has been unloaded successfully!")


def setup(client):
    client.add_cog(AdminCommands(client))