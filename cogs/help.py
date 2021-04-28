import discord
from discord.ext import commands


class Helpful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(colour= discord.Colour.orange())

        embed.set_author(name="Help Commands", icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Fun", value="`f.help fun`")
        embed.add_field(name="Helpful", value="`f.help helpful`")
        embed.add_field(name="Moderation", value="`f.help moderation`", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def moderation(self, ctx):
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name="Moderation Commands", icon_url=self.client.user.avatar_url)
        embed.add_field(name="f.exp_mute <channel>", value="Makes it so that you don't gain exp by talking in that specific channel", inline=False)
        embed.add_field(name="f.exp_unmute <channel>", value="Makes it so that you can gain exp again by talking in that specific channel", inline=False)
        embed.add_field(name="f.exp_muted", value="Shows all the currently muted channels", inline=False)
        embed.add_field(name="f.exp_multiplayer <amount>", value="Sets the speed that people gain exp", inline=False)
        embed.add_field(name="f.set_lvl <amount> <user (optional)>", value="Sets the specified user's level to the given amount. Default is your own lvl", inline=False)
        embed.add_field(name="f.set_exp <amount> <user (optional)>", value="Sets the specified user's exp to the given amount. Default is your own exp", inline=False)
        embed.add_field(name="f.give_exp <amount> <user (optional)>", value="Gives the specified user the set amount of exp. Default is your own exp", inline=False)
        embed.add_field(name="f.take_exp <amount> <user (optional)>", value="Takes the specified amount of exp from the specified user. Default is your own exp", inline=False)
        embed.add_field(name="f.clear <amount (optional)> / f.sweep / f.cls / f.clean", value="Deletes the specified amount of messages. Default is 10", inline=False)
        embed.add_field(name="f.lockdown <channel (optional)>", value="Makes the channel unable/able (toggle) to be spoken in for the verified role", inline=False)
        embed.add_field(name="f.ban <user> <reason (optional)>", value="Bans the specified person. Reason is optional", inline=False)
        embed.add_field(name="f.unban <user> <reason (optional)>", value="Unbans the specified person. Reason is optional", inline=False)
        embed.add_field(name="f.kick <user> <reason (optional)>", value="Kicks the specified person. Reason is optional", inline=False)
        embed.add_field(name="f.welcome", value="Sets a custom welcome command. Type f.welcome for more information", inline=False)
        embed.add_field(name="f.load <module>", value="Loads an command so it can be used by anyone who has the right privileges until unloaded. Note: all commands are automatically loaded when starting the bot", inline=False)
        embed.add_field(name="f.unload <module>", value="Unloads an command so it can no longer be used by anyone until reloaded", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def fun(self, ctx):
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name="Fun Commands", icon_url=self.client.user.avatar_url)
        embed.add_field(name="f.chess_challenge <time format (optional)> <user (optional)>", value="Challenge anyone or no one in particular to a chess game and play them right on discord", inline=False)
        embed.add_field(name="f.chess_puzzle <min range> <max range>", value="Recieve a chess puzzle within your set rating range to be solved right on discord", inline=False)
        embed.add_field(name="f.8ball <question> / f.magicball / f.eightball / f.enlightenme", value="Ask a question and the magic eight ball will answer you", inline=False)
        embed.add_field(name="f.slap <user>", value="Slaps the specified user", inline=False)
        embed.add_field(name="f.punch <user> / f.hit", value="Punches the specified user", inline=False)
        embed.add_field(name="f.pokedex <pokemon> / f.poke_info", value="Gets info about the specified pokemon", inline=False)
        embed.add_field(name="f.echo <message> / f.mimic / f.paste / f.say", value="Says what you say to it", inline=False)
        embed.add_field(name="f.fact", value="Tells a random fact", inline=False)
        embed.add_field(name="f.emoji <emoji>", value="Returns an appropriate(but random) emoji based on your search", inline=False)

        await ctx.send(embed=embed)

    @help.command()
    async def helpful(self, ctx):
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name="Helpful Commands", icon_url=self.client.user.avatar_url)

        embed.add_field(name="f.tag <tag name>", value="Says the tags desc if the tag exists", inline=False)
        embed.add_field(name="f.tag create <tag name> <tag desc>", value="Creates the specified tag with the specified desc", inline=False)
        embed.add_field(name="f.tag delete <tag name>", value="Deletes the specified tag", inline=False)
        embed.add_field(name="f.tag edit <tag name> <tag desc>", value="Edits the specified tag to the specified desc if you own the tag", inline=False)
        embed.add_field(name="f.tag rename <tag name> <new tag name>", value="Renames the specified tag if you own it", inline=False)
        embed.add_field(name="f.tag info <tag name>", value="Gets info on the specified tag", inline=False)
        embed.add_field(name="f.tag list <user (optional)>", value="Gets the specified person's tags if any", inline=False)
        embed.add_field(name="f.tag search %<keyword>%", value="Searches the guild's tags for the specifed keyword and sees if any tags have the keyword in their name", inline=False)
        embed.add_field(name="f.tag all", value="Gets all the tags in the guild", inline=False)

        embed.add_field(name="f.members / f.member_count / f.count", value="Tell's the current amount of members on the server", inline=False)
        embed.add_field(name="f.poll <suggestion> / f.suggestion", value="Creates a poll where people can vote by reacting", inline=False)
        embed.add_field(name="f.multi_choice <text> <choice 1> <choice 2> <etc (optional)>", value="Creates a poll where people can vote by reacting to the choices given", inline=False)
        embed.add_field(name="f.rank <user (optional)>", value="Gives you the specified users rank. Default is your own rank", inline=False)
        embed.add_field(name="f.ping", value="Returns the bot's current ping", inline=False)
        embed.add_field(name="f.whois <member (optional)>", value="Returns info on the given user. If no one is mentioned, the info of the author is given.", inline=False)
        embed.add_field(name="f.channel_status <channel (optional)> / f.channel_health / f.channel_info", value="Tells the channels health", inline=False)
        embed.add_field(name="f.report <msg>", value="Reports a msg to staff about rule breakers etc.", inline=False)
        embed.add_field(name="f.check <timeframe (optional)> <channel (optional)> <user (optional)> / f.stats / f.activity / f.messages", value="Shows the amount of messages the specified user has sent on the specified channel in the specified timeframe", inline=False)
        embed.add_field(name="f.av <mention user (optional)>", value="Shows the avatar the of the mentioned user. If no one is mentioned, the avatar of the author is returned.", inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Helpful(client))