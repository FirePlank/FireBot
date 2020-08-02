import discord, random
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fact(self, ctx):
        start = "Did you know that "
        facts = ["Banging your head against a wall for one hour burns 150 calories.",
                 "Snakes can help predict earthquakes.",
                 "7% of American adults believe that chocolate milk comes from brown cows.",
                 "If you lift a kangaroo’s tail off the ground it can’t hop.",
                 "Bananas are curved because they grow towards the sun.",
                 "Billy goats urinate on their own heads to smell more attractive to females.",
                 "The inventor of the Frisbee was cremated and made into a Frisbee after he died.",
                 "During your lifetime, you will produce enough saliva to fill two swimming pools.",
                 "Polar bears could eat as many as 86 penguins in a single sitting…",
                 "Heart attacks are more likely to happen on a Monday.",
                 "In 2017 more people were killed from injuries caused by taking a selfie than by shark attacks.",
                 "A lion’s roar can be heard from 5 miles away.",
                 "The United States Navy has started using Xbox controllers for their periscopes.",
                 "A sheep, a duck and a rooster were the first passengers in a hot air balloon.",
                 "The average male gets bored of a shopping trip after 26 minutes.",
                 "Recycling one glass jar saves enough energy to watch television for 3 hours.",
                 "Approximately 10-20% of U.S. power outages are caused by squirrels."
                ]

        fact_file = open("/app/cogs/facts.txt", mode="r", encoding="utf8")
        fact_file_facts = fact_file.read().split("\n")
        fact_file.close()

        for i in fact_file_facts:
            if i == "": fact_file_facts.remove(i)

        facts = facts + fact_file_facts

        await ctx.send(start + random.choice(facts).lower())


def setup(client):
    client.add_cog(Fun(client))