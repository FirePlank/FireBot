import discord
from discord.ext import commands
import asyncpg

class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel) or message.author.bot: return
        channel = message.channel
        messages = await channel.history(limit=3).flatten()
        if channel.id == 833089755709308988:
            msg_to_check = 1
            if messages[msg_to_check].author.bot:
                msg_to_check+=1
                num = 1
            else:
                num = int(message.content)
            if messages[msg_to_check].author == message.author:
                await channel.send(f"{message.author.mention}, Bruh don't say twice in a row. Give someone else a chance as well. Now we have to start over... From 0 we go.")
                return
            try:
                if int(messages[msg_to_check].content) + 1 != num:
                    await channel.send(f"{message.author.mention}, You just had to do it! Now we have to start over... From 0 we go.")
            except:
                await channel.send(f"{message.author.mention}, You just had to do it! Now we have to start over... From 0 we go.")

        elif channel.id == 833090029193658378:
            if len(message.content.split(" ")) > 1:
                await channel.send(f"{message.author.mention}, Bruh how hard is it to only type one word... Okay we are starting a new story, Let me start,\n\nThe")
            elif messages[1].author == message.author:
                await channel.send(
                    f"{message.author.mention}, Bruh don't say a word two times in a row... Okay we are starting a new story, Let me start,\n\nThe")

def setup(client):
    client.add_cog(AdminCommands(client))