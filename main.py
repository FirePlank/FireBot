import discord
import os
import re
import sqlite3
import datetime
from discord.ext import commands

client = commands.Bot(command_prefix = 'f.')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("f.help"))
    print("READY!")

@client.event
async def on_member_join(member):
    embed = discord.Embed(colour=discord.Colour.green(), description=f"""Welcome to {member.guild.name}, {member.mention}! You are the {len(list(member.guild.members))} member to join!

We are a great programming community wanting to help people in need.

Thank you for contributing to the server by joining and we hope you enjoy your time here!""")

    embed.set_author(name=member.name, icon_url=member.avatar_url)
    embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
    embed.timestamp = datetime.datetime.utcnow()

    await client.get_channel(id=749315830734520361).send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("The command you specified was not found. Type f.help to see all available commands.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument.")

    elif isinstance(error, discord.ext.commands.errors.MissingPermissions) or isinstance(error, discord.Forbidden):
        await ctx.send("Sorry. You don't have the permission for that command.")

    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.message.delete()
        await ctx.author.send(f"""Sorry, but we have made a cooldown to prevent spamming. Try again in {error.retry_after:,.2f} seconds.
If you want to report something before the cooldown is over or you made a report on accident then please contact a staff member and we will get it sorted out.""")

    else: await ctx.send(error)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(open("key.txt", "r").read())
