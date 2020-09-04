import discord
import datetime
import sqlite3
from discord.ext import commands

class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM welcome WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = {member.guild.id}")
        result1 = cursor.fetchone()
        if result is not None and result1 is not None:

            members = len(list(member.guild.members))
            user = member.name
            mention = member.mention
            guild = member.guild.name

            embed = discord.Embed(colour=discord.Colour.green(), description=str(result1[0]).format(members=members, mention=mention, guild=guild, user=user))

            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.set_footer(text=member.guild, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.client.get_channel(id=int(result[0]))
            await channel.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def welcome(self, ctx):
        embed = discord.Embed(colour=discord.Colour.orange())

        embed.set_author(name="Command Configuration", icon_url=self.client.user.avatar_url)
        embed.add_field(name="Welcome Message Config Options:",
                        value="f.welcome channel <#channel>\nf.welcome text <message>", inline=False)


        await ctx.send(embed=embed)

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def channel(self, ctx, channel:discord.TextChannel):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM welcome WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            sql = ("INSERT INTO welcome(guild_id, channel_id) VALUES(?,?)")
            val = (ctx.guild.id, channel.id)
            await ctx.send(f"The welcome channel has been set to {channel.mention}")

        else:
            sql = ("UPDATE welcome SET channel_id = ? WHERE guild_id = ?")
            val = (channel.id, ctx.guild.id)
            await ctx.send(f"The welcome channel has been updated to {channel.mention}")

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @welcome.command()
    @commands.has_permissions(manage_messages=True)
    async def text(self, ctx, *, text):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT msg FROM welcome WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            sql = ("INSERT INTO welcome(guild_id, msg) VALUES(?,?)")
            val = (ctx.guild.id, text)
            await ctx.send(f'The welcome message has been set to "{text}"')

        else:
            sql = ("UPDATE welcome SET msg = ? WHERE guild_id = ?")
            val = (text, ctx.guild.id)
            await ctx.send(f'The welcome message has been updated to "{text}"')

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()


def setup(client):
    client.add_cog(AdminCommands(client))
