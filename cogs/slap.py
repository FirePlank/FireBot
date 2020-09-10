from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command,cooldown
from discord import Member
from typing import Optional
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)
import os
import requests
import json
import random
import discord


class Fun(commands.Cog):

    def __init__(self, client):
        self.bot = client
        
    @command(name="slap", aliases=["hit"])
    @cooldown(1, 10, BucketType.user)
    #fun command to slap someone like pancake
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "for no reason"):
        apikey = os.environ["TENOR_API_KEY"] #set your tenorapi key from https://tenor.com/developer/dashboard ok fireplank ask me ill give you a test key
        lmt = 20
        search_term = "slap"
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt)
            )
        if r.status_code == 200:  
            top_gifs = json.loads(r.content)
            uri = random.choice(random.choice(top_gifs['results'])['media'])["gif"]["url"]
            #print(uri)
        embed = discord.Embed(
            title = f"{ctx.author.display_name} slapped {member.display_name} {reason}!",
            colour = discord.Colour.blurple()
            )

        #await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")
        embed.set_image(url=uri)
        embed.set_footer(text="Powered by Tenor")
        await ctx.send(embed=embed)
        #TODO: ERROR HANDLING

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I can't find that member")

    
def setup(client):
    client.add_cog(Fun(client))
