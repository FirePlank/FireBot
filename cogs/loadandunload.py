import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def load(self, ctx, extension):
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"The module {extension} has been loaded successfully!")
        except discord.ext.commands.errors.ExtensionNotFound:
            await ctx.send(f"The module {extension} does not exist")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reload(self, ctx, extension):
        try:
            self.client.unload_extension(f"cogs.{extension}")
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"The module {extension} has been reloaded successfully!")
        except discord.ext.commands.errors.ExtensionNotLoaded:
            await ctx.send(f"The module {extension} either is not loaded or doesn't exist")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unload(self, ctx, extension):
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"The module '{extension}' has been unloaded successfully!")
        except discord.ext.commands.errors.ExtensionNotLoaded:
            await ctx.send(f"The module {extension} either isn't loaded or doesn't exist")

def setup(client):
    client.add_cog(AdminCommands(client))