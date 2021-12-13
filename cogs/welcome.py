import discord
import datetime
from discord.ext import commands

class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        result = await self.client.pg_con.fetchrow("SELECT * FROM welcome WHERE guild_id = $1", member.guild.id)
        if result:
            members = len(list(member.guild.members))
            user = member.name
            mention = member.mention
            guild = member.guild.name

            embed = discord.Embed(colour=discord.Colour.green(), description=str(result["msg"]).format(members=members, mention=mention, guild=guild, user=user))

            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.client.get_channel(id=int(result["channel_id"]))
            await channel.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name="Command Configuration", icon_url=self.client.user.avatar_url)
        embed.add_field(name="Welcome Message Config Options:", value="f.welcome channel <#channel>\nf.welcome text <message>", inline=False)

        await ctx.send(embed=embed)

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def channel(self, ctx, channel:discord.TextChannel):
        result = await self.client.pg_con.fetchrow("SELECT * FROM welcome WHERE guild_id = $1", ctx.guild.id)

        if not result:
            await self.client.pg_con.execute("INSERT INTO welcome(guild_id, channel_id) VALUES($1,$2)", ctx.guild.id, channel.id)
            await ctx.send(f"The welcome channel has been set to {channel.mention}")

        else:
            await self.client.pg_con.execute("UPDATE welcome SET channel_id = $1 WHERE guild_id = $2", channel.id, ctx.guild.id)
            await ctx.send(f"The welcome channel has been updated to {channel.mention}")

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def text(self, ctx, *, text):
        result = await self.client.pg_con.fetchrow("SELECT * FROM welcome WHERE guild_id = $1", ctx.guild.id)

        if not result:
            await self.client.pg_con.execute("INSERT INTO welcome(guild_id, msg) VALUES($1,$2)", ctx.guild.id, text)
            await ctx.send(f'The welcome message has been set to "{text}"')

        else:
            await self.client.pg_con.execute("UPDATE welcome SET msg = $1 WHERE guild_id = $2", text, ctx.guild.id)
            await ctx.send(f'The welcome message has been updated to "{text}"')

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def check(self, ctx):
        result = await self.client.pg_con.fetchrow("SELECT * FROM welcome WHERE guild_id = $1", ctx.guild.id)

        if not result:
            msg = "NONE"
            channel = "NONE"
        else:
            if not result["msg"]: msg = "NONE"
            else: msg = result["msg"]
            if not result["channel_id"]: channel = "NONE"
            else: channel = result["channel_id"]

        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name="Command Configuration", icon_url=self.client.user.avatar_url)
        embed.add_field(name="Welcome Message Config:", value=f'The welcome channel is set to <#{channel}>\nThe welcome text set to:\n\n"{msg}"', inline=False)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(AdminCommands(client))
