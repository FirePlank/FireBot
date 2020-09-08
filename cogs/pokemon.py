import discord
from discord.ext import commands
import requests



class FunCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['pokedex'])
    async def poke_info(self, ctx, *, name):
        if len(name.split(" "))==1:
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
                data = response.json()
                
                poke_image = get_image(data)
                hp = data['base_experience']
                name = data['name'].title()
                height = str(data['height'] / 10) + "m"
                weight = str(data['weight'] / 10) + "kg"
                catagory = data['types'][0]['type']['name'].title()
                ability = [d['ability']['name'].capitalize() for d in data['abilities']]

                message = discord.Embed(title=name, color=discord.Colour.orange())

                message.set_thumbnail(url=poke_image)
                message.add_field(name="HP", value=hp)
                message.add_field(name="Height", value=height)
                message.add_field(name="Weight", value=weight)
                message.add_field(name="Catagory", value=catagory)
                message.add_field(name="Abilities", value="\n".join(ability))

                await ctx.send(embed=message)

            except:
                message = discord.Embed(title="Sorry, no Pokemon found", color=discord.Colour.orange())
                await ctx.send(embed=message)

        else:
            message = discord.Embed(title="The name cannot contain two or more words", color=discord.Colour.orange())
            await ctx.send(embed=message)


def get_image(data):
    try:
        image = data['sprites']['other']['official-artwork']['front_default']
    except:
        image = data['sprites']['front_shiny']
    return image

def setup(client):
    client.add_cog(FunCommands(client))
