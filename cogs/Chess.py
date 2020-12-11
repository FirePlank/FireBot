import discord
from discord.ext import commands

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['chess_play'])
    async def chess_invite(self, ctx, user:discord.Member):
        if user.bot:return ctx.send("You cannot invite a bot.")



def setup(client):
    client.add_cog(Fun(client))