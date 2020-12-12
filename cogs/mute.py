import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mute(self, ctx, user:discord.Member):
        muted_role = discord.utils.find(lambda r: r.name.upper() == 'MUTED', ctx.guild.roles)
        staff_role = discord.utils.find(lambda r: r.name.upper() == 'STAFF', ctx.guild.roles)
        if staff_role not in ctx.author.roles:
            return await ctx.send("Sorry. You don't have the permission for that command.")
        if staff_role in user.roles:
            return await ctx.send("You can't mute a staff member!")
        if muted_role:
            await user.add_roles(muted_role)
            await ctx.send(f"{user} has been muted.")
        else:
            await ctx.send("Couldn't find a role with 'muted' in the name.")

def setup(client):
    client.add_cog(AdminCommands(client))