import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO

async def image_helper(ctx, member, image_to_open: str, image_to_save: str,size: tuple, paste_cords: tuple,embed=False): 
    if member is None:
        member = ctx.message.author
    
    async with ctx.typing():
        if isinstance(member, discord.Member):
            image = Image.open(image_to_open)
            asset = member.avatar_url_as(size = 128)
            data = BytesIO(await asset.read())
            pfp = Image.open(data)
            resized_pfp = pfp.resize(size)
            image.paste(resized_pfp, paste_cords)
            image.save(image_to_save)
            if embed is False:
                return await ctx.send(file=discord.File(image_to_save))
            embed = discord.Embed(title=f"{member.name}", color=ctx.message.author.color)
            embed.set_image(url=f"attachment://{image_to_save}")    
            await ctx.send(content=None, embed=embed, file=discord.File(image_to_save))
        else:
            await ctx.reply("Please Mention a member!")


class Imager(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def dog(self, ctx, member=None):
            await image_helper(ctx, member, "images/dog.png", "new_dog.png", (55, 60), (178, 25), embed=True)
    
    @commands.command()
    async def wanted(self, ctx, member=None):
        await image_helper(ctx, member, "images/1.png", "new_wanted.png", (115, 120), (35, 88), embed=True)
    
    @commands.command()
    async def cheemify(self, ctx, member=None):
        await image_helper(ctx, member, "images/cheems.png", "new_cheems.png", (70, 60), (45, 35), embed=True)

    @commands.command()
    async def hoss(self, ctx, member=None):
        await image_helper(ctx, member, "images/horse.png", "new_horse.png", (40, 40), (145, 13), embed=True)
    
    @commands.command()
    async def ratify(self, ctx, member=None): 
        await image_helper(ctx, member, "images/rat.jpg", "new_rat.png", (350, 410), (60, 200), embed=True)

    @commands.command()
    async def hippofy(self, ctx, member=None):
        await image_helper(ctx, member, "images/hippo.png", "new_hippo.png", (50, 50), (160, 80), embed=True)
    
    @commands.command()
    async def grey(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        await member.avatar_url.save("images/avatar1.jpg")
        im12 = Image.open("images/avatar1.jpg").convert('L')  
        im12.save("finalim.jpg")
        embed = discord.Embed(title=f"{member.name}", color=ctx.message.author.color)
        embed.set_image(url="attachment://finalim.jpg")    
        await ctx.send(content=None, embed=embed, file=discord.File("finalim.jpg"))

def setup(client):
    client.add_cog(Imager(client))