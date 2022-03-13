import random
import requests
import math
import discord, asyncio
import os
import asyncpg
from cogs.unicode_codes import UNICODE_EMOJI
from datetime import datetime, timedelta
from cogs.perspective import perspective
import re
import time
from discord.ext import commands


class AdminCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.perspective_obj = perspective.Perspective(os.environ["perspective_api_key"])

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if isinstance(message.channel, discord.channel.DMChannel): return
        channel = message.channel

        ################################################################################################################
        #                                           BOOST CHECKER
        ################################################################################################################

        if channel.id == 836525964715884554:
            if message.author.id == 302050872383242240:
                for embed in message.embeds:
                    try:
                        if "https://disboard.org/images/bot-command-image-bump.png" == embed.to_dict()['image']['url']:
                            await self.client.pg_con.execute("UPDATE misc SET boost_timer = $1 WHERE guild_id = $2", time.time(), message.guild.id)

                            amount = 50
                            user_id = int(embed.to_dict()['description'][2:20])
                            result = await self.client.pg_con.fetchrow(
                                "SELECT * FROM levels WHERE guild_id = $1 and user_id = $2",
                                message.guild.id, user_id)
                            if result is None:
                                experience_needed = 100
                                level_at = 0

                                while amount >= experience_needed:
                                    level_at += 1
                                    amount -= experience_needed

                                await self.client.pg_con.execute(
                                    "INSERT INTO levels(guild_id, user_id, exp, lvl, last_msg) VALUES($1,$2,$3,$4,$5)",
                                    message.guild.id, user_id,
                                    amount, level_at, time.time() - 60)
                            else:
                                level_at = int(result["lvl"])
                                current_exp = int(result["exp"])
                                experience_needed = math.floor(5 * (level_at ** 2) + 50 * level_at + 100)

                                went = False
                                while amount - (experience_needed - current_exp) > 0:
                                    level_at += 1
                                    experience_needed = math.floor(5 * (level_at ** 2) + 50 * level_at + 100)
                                    amount -= experience_needed - current_exp
                                    current_exp = 0

                                if not went:
                                    amount += current_exp

                                await self.client.pg_con.execute(
                                    "UPDATE levels SET exp = $1, lvl = $2 WHERE guild_id = $3 and user_id = $4",
                                    abs(amount), level_at, message.guild.id, user_id)

                            return await channel.send(f"Congratulations <@{user_id}> for getting a 50 exp bonus for boosting!")
                    except:
                        return

        ################################################################################################################
        #                                           AUTO MODERATION
        ################################################################################################################

        channel = message.channel
        content = message.content
        staff_role = discord.utils.find(lambda r: r.name.upper() == 'STAFF', message.guild.roles)

        if str(channel) == "logs": return

        if staff_role not in message.author.roles and not message.author.bot:
            start_time = time.time()
            muted_role = discord.utils.find(lambda r: r.name.upper() == 'MUTED', message.guild.roles)

            retry = 0
            while retry < 10:
                try:
                    result = await self.client.pg_con.fetchrow(
                        "SELECT * FROM infractions WHERE guild_id = $1 AND user_id = $2", message.guild.id,
                        message.author.id)
                    break
                except asyncpg.exceptions.TooManyConnectionsError:
                    retry+=1
                    await asyncio.sleep(0.3)

            if retry >= 10: return

            if not result:
                retry = 0
                while retry < 10:
                    try:
                        await self.client.pg_con.execute(
                            "INSERT INTO infractions(guild_id, user_id, infractions, last_infraction, last_msg) VALUES($1,$2,$3,$4,$5)",
                            message.guild.id, message.author.id, 0, time.time() - 20, time.time() - 2)
                        result = await self.client.pg_con.fetchrow("SELECT * FROM infractions WHERE guild_id = $1 AND user_id = $2",
                                                                   message.guild.id, message.author.id)
                        break
                    except asyncpg.exceptions.TooManyConnectionsError:
                        retry += 1
                        await asyncio.sleep(0.3)

            infractions = 0
            if float(time.time()) - float(result['last_infraction']) > 20:
                retry = 0
                while retry < 10:
                    try:
                        await self.client.pg_con.execute(
                            "UPDATE infractions SET infractions = $1 WHERE guild_id = $2 and user_id = $3", 0,
                            message.guild.id,
                            message.author.id)

                        result = await self.client.pg_con.fetchrow(
                            "SELECT * FROM infractions WHERE guild_id = $1 AND user_id = $2", message.guild.id,
                            message.author.id)
                        break
                    except asyncpg.exceptions.TooManyConnectionsError:
                        retry += 1
                        await asyncio.sleep(0.3)

                if retry >= 10: return

            ## AUTOMOD QUICK MESSAGE
            if start_time - float(result['last_msg']) < 0.4:
                infractions += 0.4

            ## AUTOMOD EMOJI SPAM
            emojis_list = map(lambda x: ''.join(x.split()), UNICODE_EMOJI.keys())
            r = re.compile('|'.join(re.escape(p) for p in emojis_list))
            emoji_count = len(r.findall(content)) + len(re.findall(r'<a?:\w*:\d*>', content))
            if emoji_count > 5:
                infractions += emoji_count / 10 + 0.3

            ## AUTOMOD REPEATED TEXT
            repeated_check = content.replace(" ", "")
            if len(content) > 15:
                repeated = 0
                temp = (repeated_check + repeated_check).find(repeated_check, 1, -1)
                if temp != -1:
                    repeated = len(repeated_check) / temp
                infractions += round(repeated / 3.5, 2)

            ## AUTOMOD SELFBOT DETECTOR
            if message.embeds:
                infractions += 2

            ## AUTOMOD MASS PING
            mentions = len(message.mentions)
            if mentions > 2:
                mentions = len(message.raw_mentions)
                infractions += mentions - (.51 * mentions)
                infractions -= (len(content) - (22 * mentions)) * 0.005
                infractions = round(infractions, 2)

            ## AUTOMOD FILTER
            try:
                comment = self.perspective_obj.score(content, tests=["TOXICITY", "SEVERE_TOXICITY", "SEXUALLY_EXPLICIT"])
                severe_toxic = comment["SEVERE_TOXICITY"].score
                toxic = comment["TOXICITY"].score
                sexual = comment["SEXUALLY_EXPLICIT"].score
                # spam = comment["SPAM"].score

                if sexual > 0.8:
                    infractions += 0.75
                elif toxic > 0.6:
                    if severe_toxic > 0.8:
                        infractions += 0.65
                    else:
                        infractions += 0.4
                # if spam>0.5:infractions+=spam
            except:
                pass

            ## DISCORD LINK CHECK
            REGEX = re.compile('(https?:\/\/)?(www\.)?(discord\.(gg|io|me|li)|discordapp\.com\/invite)\/.+[a-z0-9]')
            links = REGEX.findall(content)
            if links:
                ignore = False
                for invite in await message.guild.invites():
                    if str(invite) == str(content).strip():
                        ignore = True
                        break
                if not ignore:
                    await message.delete()
                    infractions += 0.6

                    channel = self.client.get_channel(741011181484900464)
                    staff = discord.utils.get(message.guild.roles, id=749953613773930497)

                    embed = discord.Embed(colour=discord.Colour.red())

                    embed.add_field(name=f'__**A discord link has been detected!**__',
                                    value=f"Sender: <@{message.author.id}>", inline=False)
                    embed.add_field(name=f"Msg: {content}", value=f"Link to msg: {message.jump_url}", inline=False)
                    embed.set_footer(text=f"ID: {message.author.id}")
                    await channel.send(staff.mention, embed=embed)
                    await message.author.send(
                        f"You are not allowed to send discord invites in this server. If you believe this was a mistake please contact staff.\nYour messsage: **{content}**")

            if float(result['infractions']) + float(infractions) > 2:
                await message.author.add_roles(muted_role)

                to_del = []
                async for old_message in channel.history(limit=100, after=datetime.utcnow() - timedelta(seconds=25)):
                    if old_message.author.id == message.author.id:
                        to_del.append(old_message)
                await channel.delete_messages(to_del)

                channel = self.client.get_channel(741011181484900464)

                embed = discord.Embed(colour=discord.Colour.red(), title="__**AUTOMOD MUTE**__",
                                      icon_url=self.client.user.avatar_url,
                                      description=f"**{message.author}** has been muted for 20 minutes for getting too many mini-infractions in 20 seconds.")
                await channel.send(embed=embed)

                await message.author.send(
                    f"You have been muted in **{message.guild}** for 20 minutes for getting too many mini-infractions in 20 seconds.")

                retry = 0
                while retry < 10:
                    try:
                        await self.client.pg_con.execute(
                            "UPDATE infractions SET infractions = $1, last_infraction = $2, last_msg = $3 WHERE guild_id = $4 and user_id = $5",
                            0,
                            time.time(), time.time(), message.guild.id, message.author.id)
                        break
                    except asyncpg.exceptions.TooManyConnectionsError:
                        retry+=1
                        await asyncio.sleep(0.3)

                if retry >= 10: return

            elif infractions:
                retry = 0
                while retry < 10:
                    try:
                        await self.client.pg_con.execute(
                            "UPDATE infractions SET infractions = $1, last_infraction = $2, last_msg = $3 WHERE guild_id = $4 and user_id = $5",
                            float(infractions) + float(result['infractions']), time.time(), time.time(), message.guild.id,
                            message.author.id)
                        break
                    except asyncpg.exceptions.TooManyConnectionsError:
                        retry += 1
                        await asyncio.sleep(0.3)

                if retry >= 10: return
        
        ################################################################################################################
        #                                           SOLUTION SUBMIT
        ################################################################################################################

        if channel.id == 865193494675324928 and discord.utils.find(lambda r: r.id == 845568298669178880, message.guild.roles) not in message.author.roles:
            await message.delete()
            embed = discord.Embed(title=str(message.author), description=content)
            await self.client.guilds[0].get_channel(865192931064807454).send(embed=embed)
            await message.author.add_roles(discord.utils.find(lambda r: r.id == 865192688085499914, message.guild.roles))
            return

        ################################################################################################################
        #                                           FUN AND GAMES
        ################################################################################################################

        the_author = message.author
        if channel.id == 833089755709308988:
            if message.attachments or message.author.bot:
                await message.delete()
            else:
                messages = await channel.history(limit=2).flatten()

                try:
                    if messages[1].author == the_author or int(message.content) != int(messages[1].content) + 1:
                        await message.delete()
                except:
                    await message.delete()

        elif channel.id == 833090029193658378:
            if message.attachments or message.author.bot and the_author.id != 713789526077603850:
                await message.delete()
            else:
                messages = await channel.history(limit=7).flatten()
                for message1 in messages:
                    if message1.author.bot and the_author.id == message1.mentions[0].id:
                        if ((message.created_at-message1.created_at).total_seconds()/3600)*60*60 > 180:
                            break
                        await message.delete()
                        return

                if len(message.content.split(" ")) > 1:
                    await channel.send(f"{the_author.mention}, Bruh how hard is it to only type one word... Okay we are starting a new story, Let me start,\n\nThe")
                elif messages[1].author == the_author:
                    await channel.send(f"{the_author.mention}, Bruh don't say a word two times in a row... Okay we are starting a new story, Let me start,\n\nThe")
                elif message.content.lower() not in open("cogs/wordlist.txt", 'r').read().lower().splitlines():
                    await channel.send(f"{the_author.mention}, I don't think that's a real word... Okay we are starting a new story, Let me start,\n\nThe")

        elif channel.id == 833267391944327198 and the_author.id != 713789526077603850:
            if "```" in message.content:
                messages = await channel.history(limit=2).flatten()
                if messages[1].author == the_author:
                    await message.delete()
                    return

                if message.content.count("\n") == 0:
                    code = message.content.split("```")[1]
                else:
                    code = "\n".join(message.content.split("```")[1].split("\n")[1:]).split("```")[0]

                if code.count("\n") > 1 or code.count(";") > 1:
                    await message.delete()
                    return await channel.send(f"{the_author.mention}, please only provide a couple lines of code at once to allow other people to contribute to the program as well!")

                while True:
                    try:
                        result = await self.client.pg_con.fetchval("SELECT code FROM games WHERE guild_id = $1", message.guild.id)
                        break
                    except asyncpg.exceptions.TooManyConnectionsError:
                        await asyncio.sleep(0.3)

                if not result:
                    await self.client.pg_con.execute("INSERT INTO games(guild_id, code) VALUES($1,$2)", message.guild.id, "# code here")
                    result = "# code here"

                code = result + "\n" + code
                await self.client.pg_con.execute("UPDATE games SET code = $1 WHERE guild_id = $2", code, message.guild.id)

                await channel.send(f"Code added! Code so far:\n```py\n{code}```")

            elif message.content == "run":
                messages = await channel.history(limit=30).flatten()
                for message1 in messages:
                    if message1.author.bot:
                        for embed in message1.embeds:
                            if str(the_author) in embed.to_dict()['footer']['text']:
                                if ((message.created_at - message1.created_at).total_seconds() / 3600) * 60 * 60 < 300:
                                    return await channel.send(
                                        f"{the_author.mention}, please wait 5 minutes before using the run command again!\nThis is just because we are using a free api that has limited usage.")

                while True:
                    try:
                        result = await self.client.pg_con.fetchval("SELECT code FROM games WHERE guild_id = $1", message.guild.id)
                        break
                    except asyncpg.exceptions.TooManyConnectionsError:
                        await asyncio.sleep(0.3)

                if not result:
                    await self.client.pg_con.execute("INSERT INTO games(guild_id, code) VALUES($1,$2)", message.guild.id, "# code here")
                    result = "# code here"
                else:
                    await self.client.pg_con.execute("UPDATE games SET code = $1 WHERE guild_id = $2", "# code here", message.guild.id)

                if result == "# code here":
                    return await channel.send(f"{the_author.mention}, there is no code to run! Please provide it first.")

                data = {
                    "script": result,
                    "language": "python3",
                    "versionIndex": "3",
                    "clientId": os.environ["clientId"],
                    "clientSecret": os.environ["clientSecret"],
                    "stdin": ""
                }

                result1 = requests.post("https://api.jdoodle.com/v1/execute", json=data).json()

                if result1["statusCode"] == 200:
                    if len(result1["output"]) > 256:
                        output = result1["output"][:257]
                    else:
                        output = result1["output"]

                    if output == "":output = "No Output"

                    message = discord.Embed(title="Compilation Results", colour=discord.Colour.orange())
                    message.add_field(name="Program Output", value=f'```{output}```', inline=False)
                    message.add_field(name="Execution Time", value=result1["cpuTime"] + "s", inline=False)
                    message.set_footer(text=f"Requested by: {str(the_author)}  || Powered by Jdoodle")
                else:
                    if len(result1['error']) > 256:
                        output = result1['error'][:257]
                    else:
                        output = result1['error']

                    message = discord.Embed(title="Compilation Results", colour=discord.Colour.blue())
                    message.add_field(name="Error", value=output, inline=False)
                    message.set_footer(text=f"Requested by: {str(the_author)}  || Powered by Jdoodle")

                await channel.send(embed=message)

            elif message.content == "code":
                while True:
                    try:
                        result = await self.client.pg_con.fetchval("SELECT code FROM games WHERE guild_id = $1", message.guild.id)
                        break
                    except asyncpg.exceptions.TooManyConnectionsError:
                        await asyncio.sleep(0.3)

                await channel.send(f"Code so far:\n```py\n{str(result)}```")

            else:
                await message.delete()
                await channel.send(f"{the_author.mention}, Please only provide code you want to append to the program and nothing extra!")

        ################################################################################################################
        #                                           LEVELLING GIVER
        ################################################################################################################

        else:
            try:
                if message.content[:2] in ["f.", "p!"] or message.content[0] == ";": return
            except IndexError:
                pass
            while True:
                try:
                    result = await self.client.pg_con.fetchval(
                        "SELECT exp_muted FROM level_settings WHERE guild_id = $1", message.guild.id)
                    break
                except asyncpg.exceptions.TooManyConnectionsError:
                    await asyncio.sleep(0.3)

            if not result is None:
                if str(message.channel.id) in result: return

            author_id = message.author.id
            guild_id = message.guild.id

            while True:
                try:
                    result = await self.client.pg_con.fetchrow(
                        "SELECT * FROM levels WHERE guild_id = $1 AND user_id = $2", guild_id, author_id)
                    break
                except asyncpg.exceptions.TooManyConnectionsError:
                    await asyncio.sleep(0.3)

            if not result:
                await self.client.pg_con.execute(
                    "INSERT INTO levels(guild_id, user_id, exp, lvl, last_msg) VALUES($1,$2,$3,$4,$5)", guild_id,
                    author_id, 0, 0, time.time() - 60)
                result = await self.client.pg_con.fetchrow("SELECT * FROM levels WHERE guild_id = $1 AND user_id = $2",
                                                           guild_id, author_id)

            if time.time() - int(float(result["last_msg"])) > 60:
                result2 = await self.client.pg_con.fetchrow("SELECT * FROM level_settings WHERE guild_id = $1",
                                                            guild_id)
                if result2 is None:
                    await self.client.pg_con.execute("INSERT INTO level_settings(guild_id, multiplier) VALUES($1, $2)",
                                                     guild_id, 1)
                    result2 = await self.client.pg_con.fetchrow("SELECT * FROM level_settings WHERE guild_id = $1",
                                                                guild_id)

                exp = int(result["exp"])
                multiplier = int(result2["multiplier"])

                if len(message.content) > 100:
                    message_addon = 100 / 2.5
                else:
                    message_addon = round(len(message.content) / 2.5)
                new_exp = (exp + random.randint(10, 20) * multiplier) + message_addon
                await self.client.pg_con.execute(
                    "UPDATE levels SET exp = $1, last_msg = $2 WHERE guild_id = $3 and user_id = $4", new_exp,
                    time.time(), guild_id, author_id)

                result2 = await self.client.pg_con.fetchrow("SELECT * FROM levels WHERE guild_id = $1 AND user_id = $2",
                                                            guild_id, author_id)
                exp_start = int(result2["exp"])
                lvl_start = int(result2["lvl"])
                exp_end = math.floor(5 * (lvl_start ** 2) + 50 * lvl_start + 100)

                if exp_end < exp_start:
                    await self.client.pg_con.execute(
                        "UPDATE levels SET lvl = $1, exp = $2 WHERE guild_id = $3 and user_id = $4", lvl_start + 1,
                        exp_start - exp_end, guild_id, author_id)

                    if lvl_start + 1 == 5:
                        await message.author.add_roles(discord.utils.get(message.guild.roles,
                                                                         id=749699380214366318))  ## TODO change these hardcoded roles to server specific
                    elif lvl_start + 1 == 10:
                        await message.author.add_roles(discord.utils.get(message.guild.roles,
                                                                         id=741008881563467989))  ## TODO change these hardcoded roles to server specific
                    elif lvl_start + 1 == 20:
                        await message.author.add_roles(discord.utils.get(message.guild.roles,
                                                                         id=741008953911017553))  ## TODO change these hardcoded roles to server specific
                    elif lvl_start + 1 == 30:
                        await message.author.add_roles(discord.utils.get(message.guild.roles,
                                                                         id=752222222269284456))  ## TODO change these hardcoded roles to server specific
                    elif lvl_start + 1 == 40:
                        await message.author.add_roles(discord.utils.get(message.guild.roles,
                                                                         id=890974960766562344))  ## TODO change these hardcoded roles to server specific

def setup(client):
    client.add_cog(AdminCommands(client))
