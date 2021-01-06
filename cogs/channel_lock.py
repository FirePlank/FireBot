import discord
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        verified_role = ctx.guild.get_role(741012501445214258)

        if verified_role not in channel.overwrites:
            overwrites = {
                verified_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(embed=discord.Embed(title="This channel is now under lockdown", color=discord.Colour.orange()))
        elif channel.overwrites[verified_role].send_messages is True or \
                channel.overwrites[verified_role].send_messages is None:
            overwrites = channel.overwrites[verified_role]
            overwrites.send_messages = False
            await channel.set_permissions(verified_role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have put {channel.mention} on lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(embed=discord.Embed(title="This channel is now under lockdown.", color=discord.Colour.orange()))
        else:
            overwrites = channel.overwrites[verified_role]
            overwrites.send_messages = True
            await channel.set_permissions(verified_role, overwrite=overwrites)
            if ctx.channel != channel:
                await ctx.send(f"I have removed {channel.mention} from lockdown.")
            else:
                await ctx.message.delete()
            await channel.send(embed=discord.Embed(title="This channel is no longer under lockdown.", color=discord.Colour.orange()))


def setup(client):
    client.add_cog(AdminCommands(client))
