import discord
from discord.ext import commands
import os
import json
import random
import requests



class FunCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['poke_battle', 'battle'])
    async def poke_invite(self, ctx):
        mentions = ctx.message.mentions
        if os.path.isfile('battle_data.json'):
            await ctx.send("Sorry, there is already a battle under going.")
            return

        if len(mentions) == 0:
            await ctx.send("Please mention someone for a pokemon battle.")

        elif len(mentions) > 1:
            await ctx.send("You can't invite multiple person for a battle.")

        elif ctx.author.name == mentions[0].name:
            await ctx.send("You can't invite yourself for a battle.")

        else:
            message = discord.Embed(title="Pokemon Battle",
                                    color=discord.Colour.orange(),
                                    description=f"<@{ctx.author.id}> is inviting <@{mentions[0].id}> for a battle")

            message.add_field(name="`f.accept`", value="To enter the battle")
            message.add_field(name="`f.decline`", value="To reject the battle")                    
            
            await ctx.send(embed=message)
            data = {
                "player_1": ctx.author.name,
                "player_2": mentions[0].name
            }

            with open("battle_data.json", "w") as file:
                json.dump(data, file)


    @commands.command()
    async def accept(self, ctx):
        if os.path.isfile("battle_data.json"):
            with open("battle_data.json", "r") as file:
                data = json.load(file)
            
            if data['player_2'] == ctx.author.name:
                await ctx.send("Get Ready for a battle!")
                await self.choose(ctx)              

            elif data['player_1'] == ctx.author.name:
                await ctx.send("You are the host. You can't accept your own invitations.")

            else:
                await ctx.send("You weren't invited for the battle.")

        else:
            await ctx.send("There is no battle going on at this moment. Use `f.poke_invite <<user>>` to host a battle.")


    @commands.command()
    async def decline(self, ctx):
        if os.path.isfile("battle_data.json"):
            with open("battle_data.json", "r") as file:
                data = json.load(file)
            
            if data['player_2'] == ctx.author.name:
                await ctx.send("The battle is cancelled.")
                os.remove("battle_data.json")

            elif data['player_1'] == ctx.author.name:
                await ctx.send("The HOST decided to cancel the match.")
                os.remove("battle_data.json")

            else:
                await ctx.send("You weren't invited for the battle.")

        else:
            await ctx.send("There is no battle going on at this moment. Use `f.poke_invite <<user>>` to host a battle.")

    @commands.command()
    async def poke_leave(self, ctx):
        if os.path.isfile("battle_data.json"):
            with open("battle_data.json", "r") as file:
                data = json.load(file)

            if ctx.author.name == data['player_1']:
                await ctx.send(f"{ctx.author.mention} decided to leave the arena. And the winner is {data['player_2']}")
                os.remove("battle_data.json")
            elif ctx.author.name == data['player_2']:
                await ctx.send(f"{ctx.author.mention} decided to leave the arena. And the winner is {data['player_1']}")
                os.remove("battle_data.json")
            else:
                await ctx.send("You are not a participant.")

        else:
            await ctx.send("There is no battle going on at this moment. You can't use that command.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def poke_end(self, ctx):
        await ctx.send("The battle was force stopped by the authority.")
        try:
            os.remove("battle_data.json")
        except:
            pass

    async def choose(self, ctx):
        with open("battle_data.json", "r") as file:
            data = json.load(file)

        players = [data['player_1'], data['player_2']]
        first_player = random.choice(players)

        players.remove(first_player)

        second_player = players[0]

        data = {
            "first_move": second_player,
            "second_move": first_player,

            "player_1": {
                "player_name": first_player,
                "chosen": False
            },

            "player_2": {
                "player_name": second_player,
                "chosen": False
            }
        }

        with open("battle_data.json", "w") as file:
            json.dump(data, file)

        await ctx.send(f"{first_player}, choose your pokemon first then {second_player}. `f.poke_choose <<pokemon name>>`")
        
        
    @commands.command()
    async def poke_choose(self, ctx, *, pokemon):
        if os.path.isfile("battle_data.json"):
            with open("battle_data.json", 'r') as file:
                data = json.load(file)
            
            if not data['player_1']['chosen'] and ctx.author.name == data['player_1']['player_name']:
                if check_pokemon(pokemon):
                    with open("battle_data.json", "r") as file:
                        data = json.load(file)

                    data['player_1']['chosen'] = True

                    pokemon_data, embed_message = get_pokemon_data(pokemon)

                    data["player_1"]["pokemon"] = pokemon_data

                    with open("battle_data.json", "w") as file:
                        json.dump(data, file)

                    await ctx.send(f"{data['player_2']['player_name']}, you can choose your pokemon now.")
                    await ctx.author.send(embed=embed_message)

                else:
                    await ctx.send("No Pokemon found. Please choose your pokemon again.")

            elif not data['player_1']['chosen'] and ctx.author.name == data['player_2']['player_name']:
                await ctx.send(f"Wait for {data['player_1']['player_name']} to choose his pokemon first.")

            elif data['player_1']['chosen'] and ctx.author.name == data['player_1']['player_name']:
                await ctx.send("You have already chosen your pokemon.")
            
            elif data['player_1']['chosen'] and ctx.author.name == data['player_2']['player_name']:
                if check_pokemon(pokemon):
                    with open("battle_data.json", "r") as file:
                        data = json.load(file)

                    data['player_2']['chosen'] = True

                    pokemon_data, embed_message = get_pokemon_data(pokemon)

                    data['player_2']['pokemon'] = pokemon_data

                    with open("battle_data.json", "w") as file:
                        json.dump(data, file)

                    await ctx.author.send(embed=embed_message)

                else:
                    await ctx.send("No Pokemon found. Please choose your pokemon again.")

            elif data['player_2']['chosen'] and ctx.author.name == data['player_2']['player_name']:
                await ctx.send("You have already chosen your pokemon.")
            
        else:
            await ctx.send("There is no battle going on at this moment. You can't use this command.")


def check_pokemon(pokemon_name):
    URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    try:
        response = requests.get(URL).json()
        name = response['name'].title()
        return True
    except:
        return False


def get_pokemon_data(pokemon_name):
    URL = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(URL).json()

    pokemon_data = dict()
    pokemon_data["name"] = response["name"]
    pokemon_data["health"] = response["base_experience"]

    try:
        image_url = response['sprites']['other']['official-artwork']['front_default']
    except:
        image_url = response['sprites']['front_shiny']

    poke_moves = []
    move_names = []

    for move in response['moves']:
        tmp_dict = {
            "move_name": move['move']['name'],
            "damage": 20
        }
        move_names.append(f"{move['move']['name']} - {20}")
        poke_moves.append(tmp_dict)

    pokemon_data['moves'] = poke_moves[:4]

    embed_message = discord.Embed(title=pokemon_data["name"], color=discord.Colour.orange())
    embed_message.add_field(name="Health", value=pokemon_data["health"])
    embed_message.add_field(name="Moves", value="\n".join(move_names[:4]))
    embed_message.set_thumbnail(url=image_url)

    return pokemon_data, embed_message



def setup(client):
    client.add_cog(FunCommands(client))