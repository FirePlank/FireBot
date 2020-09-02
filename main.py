import discord
import os
import re
from discord.ext import commands

client = commands.Bot(command_prefix = 'f.')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("f.help"))
    print("READY!")

@client.event
async def on_message_delete(message):
    author = message.author # Defines the message author
    content = message.content # Defines the message content
    channel = message.channel # Defines the message channel
    if str(channel) == "logs": return
    logchannel = client.get_channel(741011181484900464) #Defines the logs channel

    embed = discord.Embed(colour=discord.Colour.purple())
    embed.add_field(name="__**Message Delete:**__", value=f"Someone (Can be themselves) deleted {author.mention}'s message in the channel {channel.mention}")
    embed.add_field(name=f'{author} said:', value=f'{content}')

    await logchannel.send(embed=embed) # Send the message.

@client.event
async def on_bulk_message_delete(messages):
    channel = messages[0].channel  # Defines the message channel
    if str(channel) == "logs": return
    logchannel = client.get_channel(741011181484900464)  # Defines the logs channel

    embed = discord.Embed(colour=discord.Colour.dark_purple())
    embed.add_field(name="__**Bulk Message Delete:**__", value=f"Channel: {channel.mention}")
    for msg in messages:
        author = msg.author # Defines the message author
        content = msg.content # Defines the message content

        embed.add_field(name=f"{author} said:", value=content, inline=False)

    await logchannel.send(embed=embed) # Send the message.

@client.event
async def on_message_edit(before, after):
    channel = before.channel  # Defines the message channel
    if str(channel) == "logs": return
    author = before.author  # Defines the message author
    if author.bot: return
    old_content = before.content  # Defines the old message content
    new_content = after.content # Defines the new message content
    logchannel = client.get_channel(741011181484900464)  # Defines the logs channel

    embed = discord.Embed(colour=discord.Colour.blurple())
    embed.add_field(name="__**Message Edit:**__", value=f"{author.mention} edited their message in the channel {channel.mention}")
    embed.add_field(name=f'{author} said:\n{old_content}', value=f'Now:\n{new_content}')

    await logchannel.send(embed=embed)  # Send the message.

@client.event
async def on_message(message):
    channel = message.channel
    if str(channel) == "logs": return
    REGEX = re.compile('(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com\/invite)\/.+[a-z0-9]')
    links = REGEX.findall(message.content)
    if links:
        channel = client.get_channel(741011181484900464)
        staff = discord.utils.get(message.guild.roles, id=749953613773930497)

        embed = discord.Embed(colour=discord.Colour.red())

        embed.add_field(name=f'__**A discord link has been detected!**__', value=f"Sender: <@{message.author.id}>", inline=False)
        embed.add_field(name=f"Msg: {message.content}", value=f"Link to msg: {message.jump_url}", inline=False)
        embed.set_footer(text=f"ID: {message.author.id}")
        await channel.send(staff.mention, embed=embed)

    await client.process_commands(message)

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
