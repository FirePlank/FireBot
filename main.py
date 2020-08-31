import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = 'f.')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(".help"))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("The command you specified was not found. Type .help to see all available commands.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument. Type .help <command> for more information.")

    elif isinstance(error, discord.ext.commands.errors.MissingPermissions) or isinstance(error, discord.Forbidden):
        await ctx.send("Sorry. You don't have the permission for that command.")

    else: await ctx.send(error)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(open("key.txt", "r").read())
