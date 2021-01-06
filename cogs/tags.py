## These commands are heavily inspired and slightly modified from the 'Tech With Tim' bot. The project github link for that can be found here: https://github.com/SylteA/Discord-Bot/


import discord, asyncio
from discord.ext import commands


class Helpful(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tag: lambda inp: inp.lower()):
        result = await self.client.pg_con.fetch("SELECT * FROM tags WHERE guild_id = $1", ctx.guild.id)
        for row in result:
            if row['title']==str(tag):
                await self.client.pg_con.execute("UPDATE tags SET use = $1 WHERE guild_id = $2 and title = $3", row['use']+1, ctx.guild.id, tag)
                return await ctx.send(row['text'])
        await ctx.send('Could not find a tag with that name.')

    @tag.command()
    @commands.has_role(741008953911017553)
    async def create(self, ctx, name: lambda inp: inp.lower(), *, text: str):
        name = await commands.clean_content().convert(ctx=ctx, argument=name)
        text = await commands.clean_content().convert(ctx=ctx, argument=text)
        result = await self.client.pg_con.fetch("SELECT * FROM tags WHERE guild_id = $1", ctx.guild.id)
        if len(result)>=50:
            return await ctx.send("You can't have more than 50 tags at the moment. Please delete your old ones that are unused with `f.tag delete [name]`")
        for row in result:
            if row['title'] == name:
                return await ctx.send("A tag with that name already exists.")
        await self.client.pg_con.execute("INSERT INTO tags(guild_id, author_id, title, text, use) VALUES($1,$2,$3,$4,$5)", ctx.guild.id, ctx.author.id, name, text, 0)
        await ctx.send("You have successfully created your tag.")

    @tag.command()
    @commands.has_role(741008953911017553)
    async def edit(self, ctx, name: lambda inp: inp.lower(), *, text: str):
        text = await commands.clean_content().convert(ctx=ctx, argument=text)
        result = await self.client.pg_con.fetch("SELECT * FROM tags WHERE guild_id = $1 and author_id = $2", ctx.guild.id, ctx.author.id)
        for row in result:
            if row['title'] == name:
                await self.client.pg_con.execute("UPDATE tags SET text = $1 WHERE guild_id = $2 and author_id = $3 and title = $4", text, ctx.guild.id, ctx.author.id, name)
                return await ctx.send("You have successfully edited your tag.")
        await ctx.send("Could not find a tag with that name in your tags.")

    @tag.command()
    @commands.has_role(741008953911017553)
    async def rename(self, ctx, name: lambda inp: inp.lower(), *, new_name: lambda inp: inp.lower()):
        new_name = await commands.clean_content().convert(ctx=ctx, argument=new_name)
        result = await self.client.pg_con.fetch("SELECT * FROM tags WHERE guild_id = $1 and author_id = $2", ctx.guild.id, ctx.author.id)
        for row in result:
            if row['title'] == name:
                await self.client.pg_con.execute("UPDATE tags SET title = $1 WHERE guild_id = $2 and author_id = $3 and title = $4", new_name, ctx.guild.id, ctx.author.id, name)
                return await ctx.send("You have successfully renamed your tag.")
        await ctx.send("Could not find a tag with that name in your tags.")

    @tag.command()
    @commands.has_role(741008953911017553)
    async def delete(self, ctx, *, tag: lambda inp: inp.lower()):
        result = await self.client.pg_con.fetch("SELECT * FROM tags WHERE guild_id = $1 and author_id = $2", ctx.guild.id, ctx.author.id)
        for row in result:
            if row['title']==tag:
                await self.client.pg_con.execute("DELETE FROM tags WHERE guild_id = $1 and author_id = $2 and title = $3", ctx.guild.id, ctx.author.id, tag)
                return await ctx.send("You have successfully deleted your tag.")
        await ctx.send("Could not find a tag with that name in your tags.")

    @tag.command()
    async def info(self, ctx, *, name: lambda inp: inp.lower()):
        result = await self.client.pg_con.fetch("SELECT * FROM tags WHERE guild_id = $1", ctx.guild.id)
        for row in result:
            if row['title'] == name:
                author = self.client.get_user(row['author_id'])
                author = str(author) if isinstance(author, discord.User) else "(ID: {})".format(row['author_id'])
                text = "Tag: {name}\n\n```prolog\nCreator: {author}\n   Uses: {uses}\n```".format(name=name, author=author, uses=row['use'])
                return await ctx.send(text)
        await ctx.send("Could not find a tag with that name.")

    @tag.command()
    async def list(self, ctx, member: commands.MemberConverter = None):
        member = member or ctx.author
        if ctx.guild.get_role(741008953911017553) not in member.roles: return await ctx.send("No tags found.")
        query = """SELECT title FROM tags WHERE guild_id = $1 AND author_id = $2 ORDER BY title"""
        records = await self.client.pg_con.fetch(query, ctx.guild.id, member.id)
        if not records:
            return await ctx.send('No tags found.')

        await ctx.send(
            f"**{len(records)} tags by {'you' if member == ctx.author else str(member)} found on this server.**"
        )

        pager = commands.Paginator()

        for record in records:
            pager.add_line(line=record["title"])

        for page in pager.pages:
            await ctx.send(page)

    @tag.command()
    @commands.cooldown(1, 3600 * 24, commands.BucketType.user)
    async def all(self, ctx: commands.Context):
        records = await self.client.pg_con.fetch(
            """SELECT title FROM tags WHERE guild_id = $1 ORDER BY title""",
            ctx.guild.id
        )

        if not records:
            return await ctx.send("This server doesn't have any tags.")

        try:
            await ctx.author.send(f"***{len(records)} tags found on this server.***")
        except discord.Forbidden:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send("Could not dm you...")

        pager = commands.Paginator()

        for record in records:
            pager.add_line(line=record["title"])

        for page in pager.pages:
            await asyncio.sleep(1)
            await ctx.author.send(page)

        await ctx.send("Tags sent in DMs.")

    @tag.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def search(self, ctx, *, term: str):
        records = await self.client.pg_con.fetch("SELECT title FROM tags WHERE guild_id = $1 AND title LIKE $2 LIMIT 10", ctx.guild.id, term)

        if not records:
            return await ctx.send(f"No tags found that has the term '{term}' in it's name")
        count = "Maximum of 10" if len(records) == 10 else len(records)
        records = "\n".join([record["title"] for record in records])

        await ctx.send(f"**{count} tags found with search term '{term}' on this server.**```\n{records}\n```")


def setup(client):
    client.add_cog(Helpful(client))