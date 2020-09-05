import discord
import random
import time
import math
import sqlite3
from discord.ext import commands

class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.content[:2] in ["f.", "p!"] or message.content[0] == ";": return
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{str(message.guild.id)}' and user_id = '{str(message.author.id)}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO levels(guild_id, user_id, exp, lvl, last_msg) VALUES(?,?,?,?, ?)")
            val = (str(message.author.guild.id), str(message.author.id), "0", "0", str(time.time()-60))
            cursor.execute(sql, val)
            db.commit()
        else:
            cursor.execute(f"SELECT user_id, exp, lvl, last_msg FROM levels WHERE guild_id = '{str(message.guild.id)}' and user_id = '{str(message.author.id)}'")
            result1 = cursor.fetchone()
            if time.time()-int(float(result1[3]))>60:
                db = sqlite3.connect("main.sqlite")
                cursor = db.cursor()
                cursor.execute(f"SELECT multiplayer FROM level_settings WHERE guild_id = '{str(message.guild.id)}'")
                result2 = cursor.fetchone()
                exp = int(result1[1])
                sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                val = (exp+random.randint(10,25)*int(result2[0]), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                sql = ("UPDATE levels SET last_msg = ? WHERE guild_id = ? and user_id = ?")
                val = (str(time.time()), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()

                cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{str(message.guild.id)}' and user_id = '{str(message.author.id)}'")
                result2 = cursor.fetchone()
                exp_start = int(result2[1])
                lvl_start = int(result2[2])
                exp_end = math.floor(5 * (lvl_start ** 2) + 50 * lvl_start + 100)

                if exp_end<exp_start:
                    await message.channel.send(f"{message.author.mention} has leveled up to level {lvl_start+1}!")
                    if lvl_start+1 == 5: await self.client.add_roles(message.author, 749699380214366318) ## TODO change these hardcoded roles to server specific
                    elif lvl_start+1 == 10: await self.client.add_roles(message.author, 741008881563467989) ## TODO change these hardcoded roles to server specific
                    elif lvl_start+1 == 20: await self.client.add_roles(message.author, 741008953911017553) ## TODO change these hardcoded roles to server specific

                    sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? and user_id = ?")
                    val = (str(lvl_start+1), str(message.guild.id), str(message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?")
                    val = (str(0+(exp_start-exp_end)), str(message.guild.id), str(message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

    @commands.command()
    async def rank(self, ctx, user:discord.User=None):
        if user is None:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{str(ctx.message.guild.id)}' and user_id = '{str(ctx.message.author.id)}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("You aren't ranked yet! Send messages to get exp.")
            else:
                embed = discord.Embed(colour=discord.Colour.orange())
                embed.set_author(name=f"{ctx.message.author.name}'s Rank", icon_url=ctx.message.author.avatar_url)
                embed.add_field(name=f"Level:", value=result[2])
                embed.add_field(name=f"EXP:", value=f"{str(result[1])}/{str(math.floor(5 * ((int(result[2])+1) ** 2) + 50 * (int(result[2])+1) + 100))}")

                await ctx.send(embed=embed)

        else:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{str(ctx.message.guild.id)}' and user_id = '{str(user.id)}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("They aren't ranked yet! They have to send messages to get exp.")
            else:
                embed = discord.Embed(colour=discord.Colour.orange())
                embed.set_author(name=f"{user.name}'s Rank", icon_url=user.avatar_url)
                embed.add_field(name=f"Level:", value=result[2])
                embed.add_field(name=f"EXP:", value=f"{result[1]}/{math.floor(5 * ((int(result[2])+1 + 1) ** 2) + 50 * (int(result[2])+1) + 100)}")

                await ctx.send(embed=embed)

        cursor.close()
        db.close()

    @commands.command()
    async def exp_multiplayer(self, ctx, number:int):
        if number > 5: await ctx.send("Sorry. The maximum multiplayer you can have is 5")
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT multiplayer FROM level_settings WHERE guild_id = '{str(ctx.message.guild.id)}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO level_settings(guild_id, multiplayer) VALUES(?,?)")
            val = (str(ctx.message.author.guild.id), 1)
            await ctx.send(f"The exp multiplayer has been set to {number}")
        else:
            sql = ("UPDATE level_settings SET multiplayer = ? WHERE guild_id = ?")
            val = (number, ctx.guild.id)
            await ctx.send(f"The exp multiplayer has been updated to {number}")

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()


def setup(client):
    client.add_cog(AdminCommands(client))