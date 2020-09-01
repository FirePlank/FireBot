import discord
from discord.ext import commands
import requests



class Fun(commands.Cog):

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

    @commands.command()
    async def emoji_id(self, ctx, *, message):
        emoji_id = message.split()
        if len(emoji_id) != 1:
            message = discord.Embed(title="Wrong ID", description=f"The given ID {' '.join(emoji_id)} is not correct")
            await ctx.send(embed=message)
        else:
            try:
                emoji_id = int(emoji_id[0])
                url = 'https://emoji.gg/assets/emoji/missingping.png'
                try:
                    emojis = requests.get('https://emoji.gg/api/').json()
                    for emoji in emojis:
                        if emoji['id'] == emoji_id:
                            url = emoji['image'].replace('discordemoji.com', 'emoji.gg')
                            break
                    await ctx.send(url)
                except:
                    pass

            except:
                await ctx.send(embed=message)


def setup(client):
    client.add_cog(Fun(client))
