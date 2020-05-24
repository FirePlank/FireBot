import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix = '.')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("📙Reading About Quantum Physics"))
    print("Ready...")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("The command you specified was not found. Type .help to see all available commands.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument. Type .help <command> for more information.")

    elif isinstance(error, discord.ext.commands.errors.MissingPermissions) or isinstance(error, discord.Forbidden):
        await ctx.send("Sorry. You don't have the permission for that command.")

    else: await ctx.send(error)


@client.command()
async def load(extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(extension):
    client.unload_extension(f"cogs.{extension}")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run('NzEzNzg5NTI2MDc3NjAzODUw.XslPeg.GYEkTwtwKL3yuG2TJKVL2pF3hFE')