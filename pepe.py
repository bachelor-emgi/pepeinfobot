from asyncio import TimeoutError, sleep
from logging import (CRITICAL, DEBUG, ERROR, INFO, WARNING, Formatter,
                     StreamHandler, getLogger)
from math import acosh, asinh, atanh, ceil, cos, cosh, e, erf, exp
from math import fabs as abs
from math import factorial, floor
from math import fmod as mod
from math import (gamma, gcd, hypot, log, log1p, log2, log10, pi, pow, sin,
                  sinh, sqrt, tan, tau)
from random import randint
from re import compile
from time import time
from urllib.parse import quote, unquote

from aiohttp import ClientSession
from art import tprint
from discord import Client, HTTPException, LoginFailure, Message, NotFound, Status
from discord.ext import tasks
from questionary import checkbox, select, text

import random
import requests

class ColourFormatter(Formatter):  # Taken from discord.py-self and modified to my liking.

    LEVEL_COLOURS = [
        (DEBUG, "\x1b[40;1m"),
        (INFO, "\x1b[34;1m"),
        (WARNING, "\x1b[33;1m"),
        (ERROR, "\x1b[31m"),
        (CRITICAL, "\x1b[41m"),
    ]

    FORMATS = {
        level: Formatter(
            f"\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s \x1b[30;1m(%(filename)s:%(lineno)d)\x1b[0m",
            "%d-%b-%Y %I:%M:%S %p",
        )
        for level, colour in LEVEL_COLOURS
    }

    def format(self, record):
        formatter = self.FORMATS.get(record.levelno)
        if formatter is None:
            formatter = self.FORMATS[DEBUG]

        if record.exc_info:
            text = formatter.formatException(record.exc_info)
            record.exc_text = f"\x1b[31m{text}\x1b[0m"

        output = formatter.format(record)

        record.exc_text = None
        return output


handler = StreamHandler()
formatter = ColourFormatter()

handler.setFormatter(formatter)
logger = getLogger("pepe")
logger.addHandler(handler)
logger.setLevel("INFO")


def cbrt(x):
    return pow(x, 1 / 3)


try:
    from ujson import dump, load
except ModuleNotFoundError:
    logger.warning("ujson not found, using json instead.")
    from json import dump, load
except ImportError:
    logger.warning("ujson not found, using json instead.")
    from json import dump, load
else:
    logger.info("ujson found, using ujson.")


channel = None


print("\033[0;35m")
tprint("PepeInfoBot", font="smslant")
print("\033[0m")

try:
    response = requests.get("https://raw.githubusercontent.com/marek-guran/pepeinfobot/main/config.json")
    config = response.json()
except Exception as e:
    print(f'Error loading config: {e}')
    config = {}

token_regex = compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27,}")
decimal_regex = compile(r"^-?\d+(?:\.\d+)$")


def validate_token(token):
    if token_regex.search(token):
        return True
    else:
        return False


def validate_decimal(decimal):
    if decimal_regex.match(decimal):
        return True
    else:
        return False


def validate_threshold_chance(s):
    try:
        threshold, chance = s.split(":")
        return (
            validate_decimal(threshold)
            and chance.isnumeric()
            and 0 <= int(chance) <= 100
        )
    except ValueError:
        if s == "":
            return True
        return False

presence_status = config.get("PRESENCE", "online").lower()
client = Client(
    status=(
        Status.invisible if presence_status == "invisible"
        else Status.online if presence_status == "online"
        else Status.idle if presence_status == "idle"
        else Status.dnd if presence_status == "dnd"
        else Status.unknown
    )
)

@client.event
async def on_ready():
    global channel
    global toad_tavern_channel
    channel = client.get_channel(config["balance_id"])
    toad_tavern_channel = client.get_channel(config["toad_tavern_id"])
    logger.info(f"Logged in as {client.user.name}#{client.user.discriminator}")
    tipping.start()
    logger.info("Tipping started.")

counter = 0
counter_a = 0
counter_b = 0
counter_c = 0
counter_f = 59

@tasks.loop(minutes=1.0)
async def tipping():
    global counter
    global counter_a
    global counter_b
    global counter_c
    global counter_f
    global config
    global response
    global toad_tavern_channel
    counter += 1
    counter_a += 1
    counter_b += 1
    counter_c += 1
    counter_f += 1
    
    # Fetch the latest config every 60 minutes
    if counter_c % 60 == 0:
        try:
            response = requests.get("https://raw.githubusercontent.com/marek-guran/pepeinfobot/main/config.json")
            response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
            config = response.json()
            logger.debug("Fetched latest config")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching config: {e}")
        counter_c = 0

    # Every 30th iteration, execute $bals top
    if counter % 30 == 0:
        await channel.send("$bals top")
        logger.debug("Sent command: $bals top")
        counter = 0
        
    if counter_b % config["time_active"] == 0:
        toad = random.choice(config["emojis"])
        toad_message = toad["emoji"]
        await toad_tavern_channel.send(toad_message)
        logger.debug(f"Sent {toad_message}")
        counter_b = 0
        
    if counter_a % config["time_announcements"] == 0:
        announcement = random.choice(config["announcements"])

        # Prepare the message
        message = announcement["Text"]
        image_url = announcement["Image"]

        # Check if there's an image URL and append it to the message
        if image_url:
            message += f"\n{image_url}"

        # Send the message to toad-tavern
        await toad_tavern_channel.send(message)
        counter_a = 0
        
    if counter_f == 60:
        # Prepare the message
        faucet1 = config["faucet1"]
        faucet2 = config["faucet2"]
        faucet1 += f"\n{faucet2}"
        await toad_tavern_channel.send(faucet1)
        logger.debug("Sent messages: faucet1 and faucet2")
        counter_f = 0

@tipping.before_loop
async def before_tipping():
    logger.info("Waiting for bot to be ready...")
    await client.wait_until_ready()

if __name__ == "__main__":
    token = "token"
    if not token:
        logger.critical("Token not found.")
        exit(1)
    try:
        client.run(token, log_handler=handler, log_formatter=formatter)
    except LoginFailure:
        logger.critical("Invalid token, restart the program.")
