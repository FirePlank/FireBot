import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs
import random



class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def emoji(self, ctx, *, message):
        URL = f"https://slackmojis.com/emojis/search?utf8=%E2%9C%93&authenticity_token=8OgBpTphVqlDDugOXU6J6IBtDdXBCdtVhg3VDCEHCTdTt7TSn5vQNha%2BoJkhDbmGkow8Tvk8d%2FiBmanqQeP%2Bdg%3D%3D&query={message}"
        response = requests.get(URL)


        if response.status_code == 200:
            soup = bs(response.text)
            images = []

            for img in soup.find_all('img'):
                images.append(img['src'])

            if len(images) != 0 and not nsfw_check(images):
                await ctx.send(random.choice(images))
            else:
                await ctx.send("Sorry, nothing for you boomer!")
        else:
            await ctx.send("Sorry, nothign for you boomer!")


def setup(client):
    client.add_cog(Fun(client))

def nsfw_check(images):
    nsfw_links = {'https://emojis.slackmojis.com/emojis/images/1528400660/4042/boob.png?1528400660',
                  'https://emojis.slackmojis.com/emojis/images/1533408970/4386/dildo.png?1533408970',
    }

    images = set(images)
    common = nsfw_links.intersection(images)
    if len(common) != 0: return True
    else: return False
