from discord.ext.commands import BucketType
from discord.ext import commands
import os
import httpx as requests
import json
import random
import discord


class FunCommands(commands.Cog):

    def __init__(self, client):
        self.bot = client
        
    @commands.command(name="slap")
    @commands.cooldown(1, 10, BucketType.user)
    async def slap_member(self, ctx, member: discord.Member):
        apikey = os.environ["TENOR_API_KEY"]
        lmt = 20
        search_term = "slap"
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        if r.status_code == 200:  
            top_gifs = json.loads(r.content)
            uri = random.choice(random.choice(top_gifs['results'])['media'])["gif"]["url"]

        else:
            embed = discord.Embed(title=f"The site was unable to be reached. Please try again later", colour=discord.Colour.blurple())
            return await ctx.send(embed=embed)

        embed = discord.Embed(title = f"{ctx.author.display_name} slapped {member.display_name}!", colour=discord.Colour.blurple())

        embed.set_image(url=uri)
        embed.set_footer(text="Powered by Tenor")
        await ctx.send(embed=embed)

    @commands.command(name="hit", aliases=["punch"])
    @commands.cooldown(1, 10, BucketType.user)
    async def hit_member(self, ctx, member: discord.Member):
        apikey = os.environ["TENOR_API_KEY"]
        lmt = 20
        search_term = "punch"
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))

        if r.status_code == 200:
            top_gifs = json.loads(r.content)
            uri = random.choice(random.choice(top_gifs['results'])['media'])["gif"]["url"]

        else:
            embed = discord.Embed(title=f"The site was unable to be reached. Please try again later", colour=discord.Colour.blurple())
            return await ctx.send(embed=embed)

        embed = discord.Embed(title=f"{ctx.author.display_name} punched {member.display_name}!", colour=discord.Colour.blurple())

        embed.set_image(url=uri)
        embed.set_footer(text="Powered by Tenor")
        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(FunCommands(client))
