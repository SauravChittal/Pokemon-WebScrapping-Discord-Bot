""" This discord bot retrives the necessary competitive set of the Pokemon
    provided in the repective tier and generation. It does so by going to a
    analysis from smogon(link present within the code). It's a webscraper.

    Imports are either for discord bot stuff or for webscraping, except time
    which is used to delay the webpage so information can be scrapped."""

import discord
from discord.ext import commands

import discobot_helper

client = discord.Client()
bot = commands.Bot(command_prefix="!")
#driver = webdriver.Chrome(ChromeDriverManager().install())

@client.event
async def on_ready():
    """Prints this line out when bot starts running"""
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    """Checks every single message to see whether the user wants some information
        or not, or displays help"""
    if message.author == client.user:
        return

    if message.content == "!!help":
        await message.channel.send("""```Type in this format /sets Pokemon (Two-Lettered
            Generation) (Tier). The things in () are optional, they automatically revert to SS 
            and/or the first tier present in analysis.
                
            Type in this format /tier Pokemon (Two-Lettered-Generation) to find out all the 
            tiers the Pokemon has analysis in. The thing in () are optionals, it automatically
            reverts to SS otherwise. Please note, the list presented might not be fully adequate
            since it depends on the users to fill out all the tiers.
            ```""")

    if message.content.startswith(r"/sets"):
        string = str(message.content)
        await message.channel.send(discobot_helper.get_sets(string))

    if message.content.startswith(r"/tier"):
        string = str(message.content)
        await message.channel.send(discobot_helper.get_tiers(string))

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    client.run(TOKEN)
