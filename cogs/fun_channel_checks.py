import discord
import random
from discord.ext import commands
import asyncpg
import requests
import os

class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        the_author = message.author
        if isinstance(message.channel, discord.channel.DMChannel) or the_author.bot: return
        channel = message.channel
        if channel.id == 833089755709308988:
            messages = await channel.history(limit=2).flatten()

            if messages[1].author == the_author or int(message.content) != int(messages[1].content) + 1:
                await message.delete()

        elif channel.id == 833090029193658378:
            article = random.choice(open("cogs/articles.txt").read().splitlines()).lower().capitalize()
            messages = await channel.history(limit=7).flatten()
            for message1 in messages:
                if message1.author.bot and the_author.id == message1.mentions[0].id:
                    if ((message.created_at-message1.created_at).total_seconds()/3600)*60*60 > 180:
                        break
                    await message.delete()
                    return

            if len(message.content.split(" ")) > 1:
                await channel.send(f"{the_author.mention}, Bruh how hard is it to only type one word... Okay we are starting a new story, Let me start,\n\n{article}")
            elif messages[1].author == the_author:
                await channel.send(f"{the_author.mention}, Bruh don't say a word two times in a row... Okay we are starting a new story, Let me start,\n\n{article}")
            elif message.content.lower() not in open("cogs/wordlist.txt", 'r').read().lower().splitlines():
                await channel.send(f"{the_author.mention}, I don't think that's a real word... Okay we are starting a new story, Let me start,\n\n{article}")

        elif channel.id == 833267391944327198:
            if "```" in message.content:
                messages = await channel.history(limit=2).flatten()
                if messages[1].author == the_author:
                    await message.delete()
                    return

                code = "\n".join(message.content.split("```")[1].split("\n")[1:-1])
                if code.count("\n") > 1:
                    return await channel.send(f"{the_author.mention}, please only provide a couple lines of code at once to allow other people to contribute to the program as well!")

                with open("cogs/code.txt", 'a') as f:
                    f.write(code + "\n")

                await channel.send(f"Code added! Code so far:\n```py\n{open('cogs/code.txt', 'r').read()}```")

            elif message.content == "run":
                with open("cogs/code.txt", 'r+') as f:
                    read_file = f.read()
                    f.truncate(0)

                if read_file == "":
                    return await channel.send(f"{the_author.mention}, there is no code to run! Please provide it first.")

                data = {
                    "script": str(read_file),
                    "language": "python3",
                    "versionIndex": "3",
                    "clientId": os.environ["clientId"],
                    "clientSecret": os.environ["clientSecret"],
                    "stdin": ""
                }

                result = requests.post("https://api.jdoodle.com/v1/execute", json=data).json()

                if result["statusCode"] == 200:
                    message = discord.Embed(title="Compilation Results", colour=discord.Colour.orange())
                    message.add_field(name="Program Output", value=f'```{result["output"]}```', inline=False)
                    message.add_field(name="Execution Time", value=result["cpuTime"], inline=False)
                    message.set_footer(text=f"Requested by: {str(the_author)}  || Powered by Jdoodle")
                else:
                    message = discord.Embed(title="Compilation Results", colour=discord.Colour.blue())
                    message.add_field(name="Error", value=result['error'], inline=False)
                    message.set_footer(text=f"Requested by: {str(the_author)}  || Powered by Jdoodle")

                await channel.send(embed=message)

            elif message.content == "code":
                messages = await channel.history(limit=30).flatten()
                for message1 in messages:
                    if message1.author.bot:
                        for embed in message1.embeds:
                            if str(the_author) in embed.to_dict()['footer']['text']:
                                if ((message.created_at - message1.created_at).total_seconds() / 3600) * 60 * 60 < 300:
                                    return await channel.send(f"{the_author.mention}, please wait 5 minutes before using the run command again!\nThis is just because we are using a free api that has limited usage.")

                with open("cogs/code.txt", 'r+') as f:
                    read_file = f.read()
                    f.truncate(0)

                await channel.send(f"Code so far:\n```py\n{read_file}```")

            else:
                await message.delete()
                await channel.send(f"{the_author.mention}, Please only provide code you want to append to the program and nothing extra!")

def setup(client):
    client.add_cog(AdminCommands(client))
