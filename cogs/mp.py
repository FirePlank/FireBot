import discord
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["preference", "thoughts", "thought", "opinion"])
    async def mp(self, ctx, person):

        if person.lower() == 'kasper':
            await ctx.send('A stupid person')

        elif person.lower() == 'arvi':
            await ctx.send("Kasper's lover boy")

        elif person.lower() == 'aapo':
            await ctx.send("A small homosexual boy")

        elif person.lower() == 'kimi':
            await ctx.send("A niger")

        elif person.lower() == 'jesse' or person.lower() == 'fireplank':
            await ctx.send("He is the best person in the entire world because he created me!")

        elif person.lower() == 'firebot':
            await ctx.send("Hey that's me! I think I am a great person if you just get to know me!")

        else: await ctx.send("I don't know who they are, but they probably are a great person!")



def setup(client):
    client.add_cog(Fun(client))