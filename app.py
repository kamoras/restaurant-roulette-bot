#!/usr/bin/python3
import os
import discord
import random
from yelp.client import Client
from yelpapi import YelpAPI

#import time

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

MY_API_KEY = "om1CsM9POR9loqdFoI52Um9hC1PyRy0QsmAP7qgvvTlkisH-0qUlR3kwJHsiX-KKQSf3mDXS0VZw60jwtC0kRyvWdzE1cA1-xH44o29W14Ks0YiRyKueggn2ViPuYXYx"


@client.event
async def on_message(message):
    """Listens for specific user messages."""
    # Current time (Used for cache busting character thumbnails).
    # epoch_time = int(time.time())

    # If the author is the bot do nothing.
    if message.author == client.user:
        return

    if message.content.startswith("!restaurant help"):
            msg = "Welcome to Restaurant Roulette! Usage:\n!restaurant roll <zipCode>"
            await message.channel.send(msg)
    elif message.content.startswith("!restaurant roll"):
        split = message.content.split()
        if len(split) < 3:
            msg = "Not enough args for restaurant roulette! Usage:\n!restaurant roll <zipCode>"
            await message.channel.send(msg)
            return

        zip_code = split[2]

        try:
            yelp_api = YelpAPI(MY_API_KEY)
            response = yelp_api.search_query(term="restaurant", location=zip_code, open_now=True, offset=0, limit=1)
            total = int(response["total"])
            offset = random.randint(0, total)
            response = yelp_api.search_query(term="restaurant", location=zip_code, open_now=True, offset=offset, limit=1)
            await message.channel.send("You should go to:\nName: " + response["businesses"][0]["name"] + "\nAddress: " + ", ".join(response["businesses"][0]["location"]["display_address"]))
        except Exception as e:
            await message.channel.send("Restaurant Roulette failed to choose a restaurant for you: " + str(e))
        finally:
            yelp_api.close()
    elif message.content.startswith("!restaurant"):
        await message.channel.send("Invalid Restaurant Roulette command. Usage:\n!restaurant roll <zipCode>")

@client.event
async def on_ready():
    print("Launch Succesful! The bot is now listening for commands...")

# Discord API Settings
DISCORD_BOT_TOKEN = str(os.environ.get("DISCORD_BOT_TOKEN"))
if DISCORD_BOT_TOKEN is None or DISCORD_BOT_TOKEN == "":
    print(
        "Missing Discord bot token. Please refer to https://github.com/JamesIves/discord-wow-armory-bot#configuration for more details"
    )
    quit()

else:
    client.run(DISCORD_BOT_TOKEN)
