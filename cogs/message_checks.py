import discord
import re
from discord.ext import commands

class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        author = message.author # Defines the message author
        content = message.content # Defines the message content
        channel = message.channel # Defines the message channel
        if str(channel) == "logs": return
        logchannel = self.client.get_channel(741011181484900464) #Defines the logs channel

        embed = discord.Embed(colour=discord.Colour.purple())
        embed.add_field(name="__**Message Delete:**__", value=f"Someone (Can be themselves) deleted {author.mention}'s message in the channel {channel.mention}")
        if message.embeds and author.bot: embed.add_field(name=f"{author} said an embed:", value="__THIS IS SUPPOSED TO BE AN EMBED__")
        else: embed.add_field(name=f'{author} said:', value=f'{content}')

        await logchannel.send(embed=embed) # Send the message.

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        channel = messages[0].channel  # Defines the message channel
        if str(channel) == "logs": return
        logchannel = self.client.get_channel(741011181484900464)  # Defines the logs channel

        embed = discord.Embed(colour=discord.Colour.dark_purple())
        embed.add_field(name="__**Bulk Message Delete:**__", value=f"Channel: {channel.mention}")
        for msg in messages:
            author = msg.author # Defines the message author
            content = msg.content # Defines the message content

            if msg.embeds and author.bot: embed.add_field(name=f"{author} said an embed:", value="**__THIS IS AN EMBED__**", inline=False)
            else: embed.add_field(name=f"{author} said:", value=content, inline=False)

        await logchannel.send(embed=embed) # Send the message.

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = before.channel  # Defines the message channel
        if str(channel) == "logs": return
        author = before.author  # Defines the message author
        if author.bot: return
        old_content = before.content  # Defines the old message content
        new_content = after.content # Defines the new message content
        if old_content == new_content: return
        logchannel = self.client.get_channel(741011181484900464)  # Defines the logs channel

        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.add_field(name="__**Message Edit:**__", value=f"{author.mention} edited their message in the channel {channel.mention}")
        embed.add_field(name=f'{author} said:', value=f'{old_content}\nNow:\n{new_content}')

        await logchannel.send(embed=embed)  # Send the message.

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        if str(channel) == "logs": return
        REGEX = re.compile('(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com\/invite)\/.+[a-z0-9]')
        links = REGEX.findall(message.content)
        if links:
            channel = self.client.get_channel(741011181484900464)
            staff = discord.utils.get(message.guild.roles, id=749953613773930497)

            embed = discord.Embed(colour=discord.Colour.red())

            embed.add_field(name=f'__**A discord link has been detected!**__', value=f"Sender: <@{message.author.id}>", inline=False)
            embed.add_field(name=f"Msg: {message.content}", value=f"Link to msg: {message.jump_url}", inline=False)
            embed.set_footer(text=f"ID: {message.author.id}")
            await channel.send(staff.mention, embed=embed)
            
        # AUTO MOD

        if len(message.mentions) >= 5:
            roles = message.guild.roles
            user = message.author

            # Check's if there is a muted role

            for role in roles:
                if role.name.upper() == "MUTED":
                    muted_role = role

            try:
                # Mutes the user is possible
                await user.add_roles(muted_role)
                await message.channel.send(
                    embed=discord.Embed(
                        title=f"Stop pinging so much {message.author.name}!",
                        color=discord.Colour.red()
                    )
                )

            except Exception:
                await message.channel.send(
                    embed=discord.Embed(
                        title="Couldn't found any **MUTED** role.",
                        color=discord.Colour.red()
                    )
                )



def setup(client):
    client.add_cog(AdminCommands(client))
