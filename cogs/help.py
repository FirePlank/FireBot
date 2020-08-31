import discord
from discord.ext import commands


class Helpful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(colour= discord.Colour.orange())


        embed.set_author(name="Help")
        embed.add_field(name="f.ping", value="Returns the bot's current ping", inline=False)
        embed.add_field(name="f.8ball <question> / f.magicball / f.eightball / f.enlightenme", value="Ask a question and the magic eight ball will answer you", inline=False)
        embed.add_field(name="f.echo <message> / f.mimic / f.paste / f.say", value="Says what you say to it", inline=False)
        embed.add_field(name="f.fact", value="Tells a random fact", inline=False)
        embed.add_field(name="f.clear <amount (optional)> / f.sweep / f.cls / f.clean", value="Deletes the specified amount of messages. Default is 10", inline=False)
        embed.add_field(name="f.channel_status / f.channel_health / f.channel_info", value="Tells the channels health", inline=False)
        embed.add_field(name="f.ban <user> <reason (optional)>", value="Bans the specified person. Reason is optional", inline=False)
        embed.add_field(name="f.unban <user> <reason (optional)>", value="Unbans the specified person. Reason is optional", inline=False)
        embed.add_field(name="f.kick <user> <reason (optional)>", value="Kicks the specified person. Reason is optional", inline=False)
        embed.add_field(name="f.check <timeframe (optional)> <channel (optional)> <user (optional)> / f.stats / f.activity / f.messages", value="Shows the amount of messages the specified user has sent on the current channel", inline=False)
        embed.add_field(name="f.load <module>", value="Loads an command so it can be used by anyone who has the right privileges until unloaded. Note: all commands are automatically loaded when starting the bot", inline=False)
        embed.add_field(name="f.unload <module>", value="Unloads an command so it can no longer be used by anyone until reloaded", inline=False)


        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Helpful(client))