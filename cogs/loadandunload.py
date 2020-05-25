import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, extension):
        self.client.load_extension(f"cogs.{extension}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, extension):
        self.client.unload_extension(f"cogs.{extension}")


def setup(client):
    client.add_cog(AdminCommands(client))