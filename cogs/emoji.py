import discord
from discord.ext import commands
import httpx as requests
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
            await ctx.send("Sorry, nothing for you boomer!")


    @commands.command()
    async def emoji_search(self, ctx, *, search):
        URL = f"https://slackmojis.com/emojis/search?utf8=%E2%9C%93&authenticity_token=8OgBpTphVqlDDugOXU6J6IBtDdXBCdtVhg3VDCEHCTdTt7TSn5vQNha%2BoJkhDbmGkow8Tvk8d%2FiBmanqQeP%2Bdg%3D%3D&query={search}"
        response = requests.get(URL)

        if response.status_code == 200:
            soup = bs(response.text)

            images = []
            titles = []

            for img in soup.find_all('img'):
                images.append(img['src'])
                title = img['alt'].replace(' random', '')
                titles.append(title)
                more_than_5 = True

            if len(images) == 0:
                await ctx.send("Sorry, nothing for you boomer!")
            elif not nsfw_check(images):
                for i in range(5):
                    message = discord.Embed(title=titles[i].title(), color=discord.Colour.orange())
                    message.set_image(url=images[i])
                    await ctx.send(embed=message)

                    if i == len(images) - 1:
                        more_than_5 = False
                        break

                if more_than_5:
                    await ctx.send(f"Type `f.emoji_list {search}` to get the full emoji list")
            else:
                message = discord.Embed(title="CENSORED!", color=discord.Colour.red())
                await ctx.send(embed=message)


    @commands.command()
    async def emoji_list(self, ctx, *, search):
        URL = f"https://slackmojis.com/emojis/search?utf8=%E2%9C%93&authenticity_token=8OgBpTphVqlDDugOXU6J6IBtDdXBCdtVhg3VDCEHCTdTt7TSn5vQNha%2BoJkhDbmGkow8Tvk8d%2FiBmanqQeP%2Bdg%3D%3D&query={search}"
        response = requests.get(URL)

        if response.status_code == 200:
            soup = bs(response.text)
            images = []
            titles = []

            common = "random"

            for img in soup.find_all('img'):
                images.append(img['src'])
                title = img['alt'].replace(" random", '')
                titles.append(title)

            if not nsfw_check(images):
                message = discord.Embed(title="Showing Emoji Search Result", color=discord.Colour.orange())
                message.add_field(name=search.title(), value=", ".join(list(set(titles))))
                
            else:
                message = discord.Embed(title="CENSORED!", color=discord.Colour.red())

            await ctx.send(embed=message)

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
