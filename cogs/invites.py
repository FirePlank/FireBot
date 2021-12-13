import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invites(self, ctx, user:discord.Member=None):
        if user is None:
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == ctx.author:
                    total_invites += i.uses
            await ctx.send(f"You've invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")
        else:
            total_invites = 0
            for i in await ctx.guild.invites():
                if i.inviter == user:
                    total_invites += i.uses

            await ctx.send(f"{user} has invited {total_invites} member{'' if total_invites == 1 else 's'} to the server!")


def setup(client):
    client.add_cog(AdminCommands(client))