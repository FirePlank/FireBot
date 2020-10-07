import discord

from discord.ext import commands
from datetime import datetime

class AmongUwUs(commands.Cogs):
    def __init__(self, client):
    self.client = client

    @commands.command(aliases=['amonguwu','au-start'])
    async def au(self, ctx, code, map, imp=2, server='europe'):
        embed = discord.Embed(
            colour=discord.Colour.red(), timestamp=ctx.message.created_at
            )
            
        embed.set_thumbnail(
            url=member.avatar_url
            )
            
        embed.set_footer(
            text=f"Requested by {ctx.author}"
            )
        
        embed.add_field(
            name=f'{ctx.author.mention} invited you to play among us'
                value=f"""
                :1234: Code: {code}
                :map: Map: {map}
                :knife: Imposter: {imp}"""
                )
        await ctx.channel.send(embed)
            

def setup(client):
    client.add_cog(AmongUwUs(client))
    