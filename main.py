import discord
import os
import asyncpg
from discord.ext import commands

client = commands.Bot(command_prefix = ['f.', 'F.'], case_insensitive=True)
client.remove_command('help')

async def create_db_pool():
    client.pg_con = await asyncpg.create_pool(host='kandula.db.elephantsql.com', user='jpwppotb', password=os.environ["database_pass"], database='jpwppotb', min_size=1, max_size=5)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("f.help"))
    print("READY!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("The command you specified was not found. Type f.help to see all available commands.")

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument.")

    elif isinstance(error, discord.ext.commands.errors.MissingPermissions) or isinstance(error, discord.Forbidden):
        await ctx.send("Sorry. You don't have the permission for that command.")

    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown) and ctx.command.name == "report":
        await ctx.message.delete()
        await ctx.author.send(f"""Sorry, but we have made a cooldown to prevent the abuse of the command. Try again in {error.retry_after:,.2f} seconds.
If you want to report something before the cooldown is over or you made a report on accident then please contact a staff member and we will get it sorted out.""")
    elif isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.send(f"You need to wait {error.retry_after:,.2f} seconds before trying this command again.")

    else: ctx.send(error)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")

client.loop.run_until_complete(create_db_pool())
client.run(os.environ["discord_token"])
