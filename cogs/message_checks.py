import discord, asyncio
import asyncpg
import time
from discord.ext import commands, tasks


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.check.start()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        author = message.author # Defines the message author
        content = message.content # Defines the message content
        channel = message.channel # Defines the message channel
        if str(channel) == "logs" or channel.id == 749525793759035414 or message.author.id == self.client.user.id: return
        logchannel = self.client.get_channel(741011181484900464) # Defines the logs channel

        embed = discord.Embed(colour=discord.Colour.purple())
        embed.add_field(name="__**Message Delete:**__", value=f"Someone (Can be themselves) deleted {author.mention}'s message in the channel {channel.mention}")
        if message.embeds and author.bot: embed.add_field(name=f"{author} said an embed:", value="__THIS IS SUPPOSED TO BE AN EMBED__")
        else: embed.add_field(name=f'{author} said:', value=f'{content}')

        await logchannel.send(embed=embed) # Send the message.

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        channel = messages[0].channel  # Defines the message channel
        if str(channel) == "logs" or channel.id == 749525793759035414: return
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
        if str(channel) == "logs" or channel.id == 749525793759035414 or after.author.id == self.client.user.id: return
        elif channel.id == 833089755709308988 or channel.id == 833090029193658378: await after.delete()
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

    @tasks.loop(seconds=20)
    async def check(self):
        while True:
            try:
                result = await self.client.pg_con.fetch("SELECT last_infraction, user_id, guild_id FROM infractions")
                break
            except asyncpg.exceptions.TooManyConnectionsError:
                await asyncio.sleep(0.3)
        for row in result:
            guild = self.client.get_guild(int(row['guild_id']))
            muted_role = discord.utils.find(lambda r: r.name.upper() == 'MUTED', guild.roles)
            user = guild.get_member(int(row['user_id']))
            if user is None:
                return await self.client.pg_con.execute("DELETE FROM infractions WHERE guild_id = $1 and user_id = $2", row['guild_id'], row['user_id'])
            if float(time.time())-float(row['last_infraction']) > 1200 and muted_role in user.roles:
                await user.remove_roles(muted_role)

        # ALSO CHECKING FOR IF ITS TIME TO BOOST CUZ THIS IS THE ONLY TASKS.LOOP :uganda:
        while True:
            try:
                result = await self.client.pg_con.fetch("SELECT boost_timer, guild_id FROM misc")
                break
            except asyncpg.exceptions.TooManyConnectionsError:
                await asyncio.sleep(0.3)

        for row in result:
            boost_time = int(row['boost_timer'])
            if time.time()-boost_time > 7200:
                guild = self.client.get_guild(int(row['guild_id']))
                channel = guild.get_channel(836525964715884554)
                await channel.send("<@&836601479665025025> it's time to boost the server! First one to do so gains 50 exp!")
                await self.client.pg_con.execute(
                    "UPDATE misc SET boost_timer = $1 WHERE guild_id = $2", time.time()-5700, guild.id)


def setup(client):
    client.add_cog(AdminCommands(client))
