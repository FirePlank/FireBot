import discord
from discord.ext import commands
import os
import json
import random
import requests



class FunCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.first_move = True

    @commands.command(aliases=['poke_battle', 'battle'])
    async def poke_invite(self, ctx):
        mentions = ctx.message.mentions
        if os.path.isfile('battle_data.json'):
            await ctx.send(embed=discord.Embed(title="Sorry, there is already a battle under going.", color=discord.Colour.red()))
            return

        if len(mentions) == 0:
            await ctx.send(embed=discord.Embed(title="Please mention someone for a pokemon battle.", color=discord.Colour.red()))

        elif len(mentions) > 1:
            await ctx.send(embed=discord.Embed(title="You can't invite multiple person for a battle.", color=discord.Colour.red()))

        elif ctx.author.name == mentions[0].name:
            await ctx.send(embed=discord.Embed(title="You can't invite yourself for a battle.", color=discord.Colour.red()))

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
                await ctx.send(embed=discord.Embed(title="Get Ready for a battle!", color=discord.Colour.orange()))
                await self.choose(ctx)              

            elif data['player_1'] == ctx.author.name:
                await ctx.send(embed=discord.Embed(title="You are the host. You can't accept your own invitations.", color=discord.Colour.red()))

            else:
                await ctx.send(embed=discord.Embed(title="You weren't invited for the battle.", color=discord.Colour.red()))

        else:
            await ctx.send(embed=discord.Embed(title="There is no battle going on at this moment. Use `f.poke_invite <<user>>` to host a battle.", color=discord.Colour.red()))


    @commands.command()
    async def decline(self, ctx):
        if os.path.isfile("battle_data.json"):
            with open("battle_data.json", "r") as file:
                data = json.load(file)
            
            if data['player_2'] == ctx.author.name:
                await ctx.send(embed=discord.Embed(title="The battle is cancelled.", color=discord.Colour.red()))
                os.remove("battle_data.json")

            elif data['player_1'] == ctx.author.name:
                await ctx.send(embed=discord.Embed(title="The HOST decided to cancel the match.", color=discord.Colour.red()))
                os.remove("battle_data.json")

            else:
                await ctx.send(embed=discord.Embed(title="You weren't invited for the battle.", color=discord.Colour.red()))

        else:
            await ctx.send(embed=discord.Embed(title="There is no battle going on at this moment. Use `f.poke_invite <<user>>` to host a battle.", color=discord.Colour.red()))

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
        try:
            os.remove("battle_data.json")
            await ctx.send("The battle was force stopped by the authority.")
        except:
            await ctx.send(f"There is no battle")

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
                await ctx.message.delete()
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
                await ctx.message.delete()
                if check_pokemon(pokemon):
                    with open("battle_data.json", "r") as file:
                        data = json.load(file)

                    data['player_2']['chosen'] = True

                    pokemon_data, embed_message = get_pokemon_data(pokemon)

                    data['player_2']['pokemon'] = pokemon_data

                    with open("battle_data.json", "w") as file:
                        json.dump(data, file)

                    await ctx.author.send(embed=embed_message)
                    await ctx.send(f"It's {data['first_move']}'s turn! do `f.poke_use (move)` to use an move and `f.poke_moves` to see all your available moves.")

                else:
                    await ctx.send("No Pokemon found. Please choose your pokemon again.")

            elif data['player_2']['chosen'] and ctx.author.name == data['player_2']['player_name']:
                await ctx.send("You have already chosen your pokemon.")
            
        else:
            await ctx.send("There is no battle going on at this moment. You can't use this command.")


    @commands.command()
    async def poke_use(self, ctx, move):
        match_ended = False
        if os.path.isfile("battle_data.json"):
            with open("battle_data.json", 'r') as file:
                data = json.load(file)

                if not data["player_1"]["chosen"] or not data["player_2"]["chosen"]:
                    await ctx.send("Not everyone has chosen their pokemon's yet!")
                    return
                if data["first_move"] != str(ctx.author.name) and data["second_move"] != str(ctx.author.name):
                    await ctx.send("You are not an participant of this battle!")
                    return
                if self.first_move and data["first_move"] != str(ctx.author.name) or not self.first_move and data["second_move"] != str(ctx.author.name):
                    await ctx.send("It's not your turn yet!")
                    return

                if self.first_move and data["first_move"] == data["player_1"]["player_name"]:
                    mover = "player_1"
                    not_mover = "player_2"
                else:
                    mover = "player_2"
                    not_mover = "player_1"
                if self.first_move:
                    moves = data[mover]["pokemon"]["moves"]
                    if move == moves[0]["move_name"]: move_dmg = moves[0]["damage"]
                    elif move == moves[1]["move_name"]: move_dmg = moves[1]["damage"]
                    elif move == moves[2]["move_name"]: move_dmg = moves[2]["damage"]
                    elif move == moves[3]["move_name"]: move_dmg = moves[3]["damage"]
                    else:
                        await ctx.send("You don't have that move! Type `f.poke_moves` to see all of your available moves")
                        return
                else:
                    moves = data[not_mover]["pokemon"]["moves"]
                    if move == moves[0]["move_name"]: move_dmg = moves[0]["damage"]
                    elif move == moves[1]["move_name"]: move_dmg = moves[1]["damage"]
                    elif move == moves[2]["move_name"]: move_dmg = moves[2]["damage"]
                    elif move == moves[3]["move_name"]: move_dmg = moves[3]["damage"]
                    else:
                        await ctx.send("You don't have that move! Type `f.poke_moves` to see all of your available moves")
                        return

                if self.first_move:
                    self.first_move=False
                    data[not_mover]["pokemon"]["health"] = int(data[not_mover]["pokemon"]["health"]) - move_dmg

                    with open("battle_data.json", "w") as file:
                        json.dump(data, file)

                    if int(data[not_mover]["pokemon"]["health"]) <= 0:
                        await ctx.send(f"{ctx.author.name} wins! {data['second_move']}'s pokemon has no health left.")
                        match_ended = True
                        return
                    else:
                        await ctx.send(f"{ctx.author.name} used {move} and dealt {move_dmg} dmg!")
                        await ctx.send(f"{data[not_mover]['player_name']}'s pokemon {data[not_mover]['pokemon']['name']} has {data[not_mover]['pokemon']['health']} health left")
                        await ctx.send(f"It's {data['second_move']}'s turn! do `f.poke_use (move)` to use an move and `f.poke_moves` to see all your available moves.")

                else:
                    self.first_move=True
                    data[mover]["pokemon"]["health"]=int(data[mover]["pokemon"]["health"])-move_dmg

                    with open("battle_data.json", "w") as file:
                        json.dump(data, file)

                    if int(data[mover]["pokemon"]["health"]) <= 0:
                        await ctx.send(f"{ctx.author.name} wins! {data['first_move']}'s pokemon has no health left.")
                        match_ended = True
                        
                    else:
                        await ctx.send(f"{ctx.author.name} used {move} and dealt {move_dmg} dmg!")
                        await ctx.send(f"{data[mover]['player_name']}'s pokemon {data[mover]['pokemon']['name']} has {data[mover]['pokemon']['health']} health left")
                        await ctx.send(f"It's {data['first_move']}'s turn! do `f.poke_use (move)` to use an move and `f.poke_moves` to see all your available moves.")


        else:
            await ctx.send("There is no battle going on at this moment. You can't use this command.")

        if match_ended:
            os.remove("battle_data.json")


    @commands.command(aliases=['pokedex'])
    async def poke_info(self, ctx, *, name):
        if len(name.split(" ")) == 1:
            try:
                response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}")
                data = response.json()

                poke_image = get_image(data)
                hp = data['base_experience']
                name = data['name'].title()
                height = str(data['height'] / 10) + "m"
                weight = str(data['weight'] / 10) + "kg"
                category = data['types'][0]['type']['name'].title()
                ability = [d['ability']['name'].capitalize() for d in data['abilities']]

                message = discord.Embed(title=name, color=discord.Colour.orange())

                message.set_thumbnail(url=poke_image)
                message.add_field(name="HP", value=hp)
                message.add_field(name="Height", value=height)
                message.add_field(name="Weight", value=weight)
                message.add_field(name="Category", value=category)
                message.add_field(name="Abilities", value="\n".join(ability))

                await ctx.send(embed=message)

            except:
                message = discord.Embed(title="Sorry, no Pokemon found", color=discord.Colour.orange())
                await ctx.send(embed=message)

        else:
            message = discord.Embed(title="The name cannot contain two or more words", color=discord.Colour.orange())
            await ctx.send(embed=message)


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
    pokemon_data["health"] = response["stats"][0]["base_stat"]

    try:
        image_url = response['sprites']['other']['official-artwork']['front_default']
    except:
        image_url = response['sprites']['front_shiny']

    poke_moves = []
    move_names = []

    for i, move in enumerate(response['moves']):
        url = move["move"]["url"]
        response = requests.get(url).json()
        if response["power"] is None: power = 20
        else: power = round(int(response["power"])/3)

        tmp_dict = {
            "move_name": move['move']['name'],
            "damage": power,
            "move_index": i+1
        }
        move_names.append(f"{move['move']['name']} - {power}")
        poke_moves.append(tmp_dict)

        if i == 3:
            break

    pokemon_data['moves'] = poke_moves[:4]

    embed_message = discord.Embed(title=pokemon_data["name"], color=discord.Colour.orange())
    embed_message.add_field(name="Health", value=pokemon_data["health"])
    embed_message.add_field(name="Moves", value="\n".join(move_names[:4]))
    embed_message.set_thumbnail(url=image_url)

    return pokemon_data, embed_message

def get_image(data):
    try:
        image = data['sprites']['other']['official-artwork']['front_default']
    except:
        image = data['sprites']['front_shiny']
    return image


def setup(client):
    client.add_cog(FunCommands(client))