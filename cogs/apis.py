from discord.ext import commands
import requests
import discord
from bs4 import BeautifulSoup

async def temperature(ctx, city):
  googleurl = "https://google.com/search?q=weather+in+" + city
  request_result = requests.get(googleurl)

  soup = BeautifulSoup( request_result.text
	  				, "html.parser" )
  temp = soup.find( "div" , class_='BNeawe' ).text
  tempEmbed = discord.Embed(title=city.capitalize(), description=temp, color=ctx.message.author.color) 
  
  await ctx.send(content=None, embed=tempEmbed)


async def meaning(ctx, word):
      url = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
      try:
        content = url.json()[0]
  
        embed = discord.Embed(title=word.capitalize(), color=ctx.message.author.color)
      except:
        await ctx.send("Word Not Found")
        return
      try:    
        info = content["meanings"][0]["definitions"][0]["definition"]
      except:
        info = "Not Defined"
      try:
        synonym = content["meanings"][0]["definitions"][0]["synonyms"][0]
      except:
        synonym = "No Synonym"
      try:
        antonym = content["meanings"][0]["definitions"][0]["antonyms"][0]
      except:
        antonym = "No Antonym"
    
      embed.add_field(name="Meaning", value=info.capitalize(), inline=False)
      embed.add_field(name="Synonym", value=synonym.capitalize(), inline=False)
      embed.add_field(name="Antonym", value=antonym.capitalize(), inline=False)
      await ctx.send(embed=embed)


class API(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def quote(self, ctx):
        async with ctx.typing():
            response = requests.get("https://zenquotes.io/api/random")
            data = response.json()
            quote = data[0]["q"]
            author = data[0]["a"]
            await ctx.send(f"**{quote}**- *{author}*")

    @commands.command(aliases=["def"])
    async def mean(self, ctx, *, word):
        async with ctx.typing():
            await meaning(ctx, word)

    @commands.command(aliases=["temperature"])
    async def temp(self, ctx, *, city):
      async with ctx.typing():
        await temperature(ctx, city)


def setup(client):
    client.add_cog(API(client))