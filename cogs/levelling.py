import discord
import random
import time
import math
import asyncpg, asyncio
from discord.ext import commands
class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rank(self, ctx, user:discord.User=None):
        if user is None:
            result = await self.client.pg_con.fetchrow("SELECT * FROM levels WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, ctx.author.id)
            if not result:
                await ctx.send("You aren't ranked yet! Send messages to get exp.")
            else:
                embed = discord.Embed(colour=discord.Colour.orange())
                embed.set_author(name=f"{ctx.message.author.name}'s Rank", icon_url=ctx.message.author.avatar_url)
                embed.add_field(name=f"Level:", value=result["lvl"])
                embed.add_field(name=f"EXP:", value=f"{str(result['exp'])}/{math.floor(5 * ((int(result['lvl'])+1) ** 2) + 50 * (int(result['lvl'])+1) + 100)}")

                await ctx.send(embed=embed)

        else:
            result = await self.client.pg_con.fetchrow("SELECT * FROM levels WHERE guild_id = $1 AND user_id = $2", ctx.guild.id, user.id)
            if not result:
                await ctx.send("They aren't ranked yet! They have to send messages to get exp.")
            else:
                embed = discord.Embed(colour=discord.Colour.orange())
                embed.set_author(name=f"{user.name}'s Rank", icon_url=user.avatar_url)
                embed.add_field(name=f"Level:", value=result["lvl"])
                embed.add_field(name=f"EXP:", value=f"{result['exp']}/{math.floor(5 * ((int(result['lvl'])+1) ** 2) + 50 * (int(result['lvl'])+1) + 100)}")

                await ctx.send(embed=embed)

    @commands.command(aliases=["lb, top"])
    async def leaderboard(self, ctx):
        result = await self.client.pg_con.fetchall("SELECT * FROM levels WHERE guild_id = $1", ctx.guild.id)

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def exp_multiplier(self, ctx, number:float):
        if number > 5:
            await ctx.send("Sorry. The maximum multiplier you can have is 5")
            return
        result = await self.client.pg_con.fetchval("SELECT multiplier FROM level_settings WHERE guild_id = $1", ctx.guild.id)
        if result is None:
            await self.client.pg_con.execute("INSERT INTO level_settings(guild_id, multiplier) VALUES($1,$2)", ctx.guild.id, number)
            await ctx.send(f"The exp multiplier has been set to {number}")
        else:
            await self.client.pg_con.execute("UPDATE level_settings SET multiplier = $1 WHERE guild_id = $2", number, ctx.guild.id)
            await ctx.send(f"The exp multiplier has been updated to {number}")

    @commands.command(aliases=["set_level", "set_rank"])
    @commands.has_permissions(manage_guild=True)
    async def set_lvl(self, ctx, amount:int, *, user:discord.User=None):
        if user is None: user = ctx.author
        guild_id = ctx.guild.id

        result = await self.client.pg_con.fetchval("SELECT lvl FROM levels WHERE guild_id = $1 and user_id = $2", guild_id, user.id)

        if result is None:
            await self.client.pg_con.execute("INSERT INTO levels(guild_id, user_id, exp, lvl, last_msg) VALUES($1,$2,$3,$4,$5)",  guild_id, user.id, 0, amount, time.time()-60)
        else:
            await self.client.pg_con.execute("UPDATE levels SET lvl = $1 WHERE guild_id = $2 and user_id = $3", amount, guild_id, user.id)
        await ctx.send(f"{user.name}'s level has been set to {amount}")

    @commands.command(aliases=["set_experience"])
    @commands.has_permissions(manage_guild=True)
    async def set_exp(self, ctx, amount: int, *, user: discord.User = None):
        if user is None: user = ctx.author
        guild_id = ctx.guild.id

        result = await self.client.pg_con.fetchrow("SELECT * FROM levels WHERE guild_id = $1 and user_id = $2", guild_id, user.id)
        if result is None:
            if amount>=100:
                await ctx.send("You cannot set more exp than their current level exp requirement is")
                return
            await self.client.pg_con.execute("INSERT INTO levels(guild_id, user_id, exp, lvl, last_msg) VALUES($1,$2,$3,$4,$5)", guild_id, user.id, amount, 0, time.time() - 60)
        else:
            if amount>=math.floor(5*((int(result["lvl"])+1)**2)+50*(int(result["lvl"])+1)+100):
                await ctx.send("You cannot set more exp than their current level exp requirement is")
                return
            await self.client.pg_con.execute("UPDATE levels SET exp = $1 WHERE guild_id = $2 and user_id = $3", amount, guild_id, user.id)

        await ctx.send(f"{user.name}'s exp has been set to {amount}")

    @commands.command(aliases=["give_experience"])
    @commands.has_permissions(manage_guild=True)
    async def give_exp(self, ctx, amount: int, *, user: discord.Member = None):
        if user is None: user = ctx.author
        guild_id = ctx.guild.id

        result = await self.client.pg_con.fetchrow("SELECT * FROM levels WHERE guild_id = $1 and user_id = $2",
                                                   guild_id, user.id)
        if result is None:
            experience_needed = 100
            level_at = 0

            while amount >= experience_needed:
                level_at+=1
                amount -= experience_needed

            await self.client.pg_con.execute(
                "INSERT INTO levels(guild_id, user_id, exp, lvl, last_msg) VALUES($1,$2,$3,$4,$5)", guild_id, user.id,
                amount, level_at, time.time() - 60)
        else:
            level_at = int(result["lvl"])
            current_exp = int(result["exp"])
            experience_needed = math.floor(5 * (level_at ** 2) + 50 * level_at + 100)

            went = False
            while amount - (experience_needed - current_exp) > 0:
                level_at+=1
                experience_needed = math.floor(5 * (level_at ** 2) + 50 * level_at + 100)
                amount-=experience_needed - current_exp
                current_exp=0

            if not went:
                amount+=current_exp

            await self.client.pg_con.execute("UPDATE levels SET exp = $1, lvl = $2 WHERE guild_id = $3 and user_id = $4", abs(amount), level_at, guild_id, user.id)

        await ctx.send(f"{user.name} has been given the specified amount of experience.")

    @commands.command(aliases=["take_experience"])
    @commands.has_permissions(manage_guild=True)
    async def take_exp(self, ctx, amount: int, *, user: discord.Member = None):
        if user is None: user = ctx.author
        guild_id = ctx.guild.id

        result = await self.client.pg_con.fetchrow("SELECT * FROM levels WHERE guild_id = $1 and user_id = $2", guild_id, user.id)

        if result is None:
            return await ctx.send(f"{user.name} has no experience or levels to begin with!")

        else:
            level_at = int(result["lvl"])
            current_exp = int(result["exp"])

            while amount - current_exp > 0:
                amount -= current_exp
                current_exp = math.floor(5 * (level_at ** 2) + 50 * level_at + 100)
                level_at -= 1

            current_exp -= amount

            await self.client.pg_con.execute(
                "UPDATE levels SET exp = $1, lvl = $2 WHERE guild_id = $3 and user_id = $4", abs(current_exp), level_at,
                guild_id, user.id)

        await ctx.send(f"{user.name} has been taken the specified amount of experience.")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def exp_mute(self, ctx, channel:discord.TextChannel):
        result = await self.client.pg_con.fetchrow("SELECT * FROM level_settings WHERE guild_id = $1", ctx.guild.id)
        if result["exp_muted"] is None: await self.client.pg_con.execute("UPDATE level_settings SET exp_muted = $1 WHERE guild_id = $2", [str(channel.id)], ctx.guild.id)
        else:
            lst = result["exp_muted"]
            lst.append(str(channel.id))
            await self.client.pg_con.execute("UPDATE level_settings SET exp_muted = $1 WHERE guild_id = $2", lst, ctx.guild.id)

        await ctx.send(f"{channel.mention} is now exp muted")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def exp_unmute(self, ctx, channel: discord.TextChannel):
        result = await self.client.pg_con.fetchrow("SELECT * FROM level_settings WHERE guild_id = $1", ctx.guild.id)
        if result["exp_muted"] is None: await ctx.send("You haven't exp muted anything!")
        else:
            lst = result["exp_muted"]
            if str(channel.id) not in lst: await ctx.send(f"The channel {channel.mention} is not currently exp muted")
            else:
                lst.remove(str(channel.id))
                await self.client.pg_con.execute("UPDATE level_settings SET exp_muted = $1 WHERE guild_id = $2", lst, ctx.guild.id)
                await ctx.send(f"{channel.mention} is no longer exp muted")

    @commands.command()
    async def exp_muted(self, ctx):
        result = await self.client.pg_con.fetchval("SELECT exp_muted FROM level_settings WHERE guild_id = $1", ctx.guild.id)
        lst = []
        for i in result:
            lst.append(f"<#{str(i)}>")

        embed = discord.Embed(colour=discord.Colour.orange(), description=", ".join(lst))
        embed.set_author(name=f"Exp Muted Channels", icon_url=self.client.user.avatar_url)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(AdminCommands(client))