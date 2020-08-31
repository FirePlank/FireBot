import discord
from discord.ext import commands
import requests



class EmojiCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def emoji(self, ctx, *, message):
        emoji_name = message.split()
        emoji_name = '_'.join(emoji_name)
        url = 'https://emoji.gg/assets/emoji/missingping.png'

        try:
            emojis = requests.get('https://emoji.gg/api/').json()
            for emoji in emojis:
                catagory = emoji['category']
                if emoji_name.lower() in emoji['title'].lower() and catagory != 9:
                    url = emoji['image']
                    url = url.replace('discordemoji.com', 'emoji.gg')
                    print(emoji['image'])
                    break
            
        except Exception as e:
            print(e)

        await ctx.send(url)


def setup(client):
    client.add_cog(EmojiCommands(client))
