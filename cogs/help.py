import discord
from discord.ext import commands


class Helpful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):

        embed = discord.Embed(colour= discord.Colour.orange())


        embed.set_author(name="Help")
        embed.add_field(name=".ping", value="Returns the bot's current ping", inline=False)
        embed.add_field(name=".8ball / .magicball / .eightball / .enlightenme", value="Ask a question and the magic eight ball will answer you", inline=False)
        embed.add_field(name=".echo", value="Says what you say to it", inline=False)
        embed.add_field(name=".fact", value="Tells a random fact", inline=False)
        embed.add_field(name=".clear / .sweep / .cls / .clean", value="Deletes the specified amount of messages. Default is 10", inline=False)
        embed.add_field(name=".ban", value="Bans the specified person. Reason is optional", inline=False)
        embed.add_field(name=".unban", value="Unbans the specified person. Reason is optional", inline=False)
        embed.add_field(name=".kick", value="Kicks the specified person. Reason is optional", inline=False)
        embed.add_field(name=".load", value="Loads an command so it can be used by anyone who has the right privileges until unloaded. Note: all commands are automatically loaded when starting the bot", inline=False)
        embed.add_field(name=".unload", value="Unloads an command so it can no longer be used by anyone until reloaded", inline=False)


        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Helpful(client))