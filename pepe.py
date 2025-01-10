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
    config = {
    "PRESENCE": "online",
    "balance_id": 1260500212628066316,
    "toad_tavern_id": 1203748781590577222,
    "goon_market_id": 1326007045136187514,
    "time_active": 29,
    "time_announcements": 180,
    "time_goon": 29,
    "announcements": [
        {
            "Text": " ### Ever wanted to earn Pepecoins by playing games? [Flappy PEPE]( https://flappypepe.com/ ) has one of the first Pepecoin games! You can earn by playing some Pepe!",
            "Image": ""
        },
        {
            "Text": " # <:Pepe_King:1212645776975732767> Reminder that Pepecoin has Faucets! <:Pepe_money:1208212886606979093> ",
            "Image": " [Pepeblocks]( <https://faucet.pepeblocks.com/> ), [Ravener]( <https://pepe.ravener.is-a.dev/> ) "
        },
        {
            "Text": "New to Pepecoin? Find out what it is in <#1195861340347170877>",
            "Image": ""
        },
        {
            "Text": "Ever asked yourself how could you get hold of Pepecoin? Head over to <#1248806239949819905>",
            "Image": ""
        },
        {
            "Text": "Keep in touch with us! Follow us on our <#1257093939786289223>",
            "Image": ""
        },
        {
            "Text": "Need help? Ask anything in <#1225259101257334824> and we will get in touch with you",
            "Image": ""
        },
        {
            "Text": "Stay safe from scams! Nobody from the team will message you to give you any support! Report these users in <#1195281617799872582>",
            "Image": ""
        },
        {
            "Text": "Any idea for improvement? Tell us your idea in <#1199307065500389417>",
            "Image": ""
        },
        {
            "Text": "<#1181472510370386001> are the guardrails on the road of life, ensuring that we stay on the right path and avoid the pitfalls that could cost us consequences.",
            "Image": ""
        },
        {
            "Text": "Check <#1181708314841731193> and <#1258272895679856700> for new information about Pepecoin ",
            "Image": ""
        },
        {
            "Text": "Want to mine, but don't know how? Join <#1195950853249564802> and ask for help!",
            "Image": ""
        },
        {
            "Text": "When backing up your wallet.dat file, ensure it's securely stored in multiple locations. If you encrypt your wallet, remember that your password is the key to your assets - lose it, and you lose access to your funds. Backup responsibly, and safeguard your password diligently.",
            "Image": ""
        },
        {
            "Text": "New to Pepecoin? Don't know how to start? Head to [Pepelum](<https://pepelum.site/>) - Pepecoin guide by community member: Mr Bachelor emgi",
            "Image": ""
        },
        {
            "Text": "Did you know we have Telegram group? Oh yes! And we  also have a Pepecoin tip bot there! Join here: [Pepecoin]( https://t.me/PepecoinGroup )",
            "Image": ""
        },
        {
            "Text": "Anyone can drop coins, even a small amount is welcome",
            "Image": ""
        }
    ],
    "goon_messages": [
        {
            "Text": " ### Warning! <:Pepe_police:1196127014936133763> ",
            "Image": "> Goon Market chat stays here! You are not allowed to move goon theme to other channels as it will be considered intentional rules breaking."
        }
    ],
    "emojis": [
        {
            "emoji": " <:PepeCrypto:1195369274496258118> "
        },
        {
            "emoji": " <:Pepe_Evil:1195369327910715482> "
        },
        {
            "emoji": " <:Pepe_King:1212645776975732767> "
        },
        {
            "emoji": " <:Pepe_money:1208212886606979093> "
        },
        {
            "emoji": " <:chefpepe:1259261034661810258> "
        },
        {
            "emoji": " <:elon_pepe:1240106148296917052> "
        },
        {
            "emoji": " <:exploring_pepe:1226021496233791588> "
        },
        {
            "emoji": " <:feelsratman:1195069924473835520> "
        },
        {
            "emoji": " <:mining_pepe:1224934623247597578> "
        },
        {
            "emoji": " <:peepo_wave:1208212638530801664> "
        },
        {
            "emoji": " <:peepoblanket:1212645178138034176> "
        },
        {
            "emoji": " <:peepolike:1212644960164118528> "
        },
        {
            "emoji": " <:pepe_heart:1202072882252087366> "
        },
        {
            "emoji": " <:pepe_hug:1208212685087309834> "
        },
        {
            "emoji": " <:pepe_love:1208212840511442974> "
        },
        {
            "emoji": " <:pepe_meditate:1208212861084766289> "
        },
        {
            "emoji": " <:pepe_shh:1196481393551745148> "
        },
        {
            "emoji": " <:pepe_smile:1208212936393228350> "
        },
        {
            "emoji": " <:pepe_stocks:1195369423528271873> "
        },
        {
            "emoji": " <:pepe_thuglife:1208212980223971338> "
        },
        {
            "emoji": " <:pepebuffclown:1195070259414192138> "
        },
        {
            "emoji": " <:pepebussines:1195070283892138065> "
        },
        {
            "emoji": " <:pepecoin:1238351047181996062> "
        },
        {
            "emoji": " <:pepecomfyblush:1195369461922926915> "
        },
        {
            "emoji": " <:pepecool:1212644987288813639> "
        },
        {
            "emoji": " <:pepege:1195070470354112545> "
        },
        {
            "emoji": " <:pepehappy:1195070531830042755> "
        },
        {
            "emoji": " <:pepeheh:1196127045877502012> "
        },
        {
            "emoji": " <:pepehmmm:1195070548485607505> "
        },
        {
            "emoji": " <:pepejudge:1195369594450358312> "
        },
        {
            "emoji": " <:pepepopcorn:1212644628294008864> "
        },
        {
            "emoji": " <:pepesip:1195369615191191582> "
        },
        {
            "emoji": " <:pepesipsmug:1196127067549466624> "
        },
        {
            "emoji": " <:pepetosto:1195071168806408263> "
        }
    ]
}

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
    global goon_market_channel
    channel = client.get_channel(config["balance_id"])
    toad_tavern_channel = client.get_channel(config["toad_tavern_id"])
    goon_market_channel = client.get_channel(config["goon_market_id"])
    logger.info(f"Logged in as {client.user.name}#{client.user.discriminator}")
    tipping.start()
    logger.info("Tipping started.")

counter = 0
counter_a = 0
counter_b = 28
counter_c = 0
counter_g = 0

@tasks.loop(minutes=1.0)
async def tipping():
    global counter
    global counter_a
    global counter_b
    global counter_c
    global counter_g
    global config
    global response
    global toad_tavern_channel
    global goon_market_channel
    counter += 1
    counter_a += 1
    counter_b += 1
    counter_c += 1
    counter_g += 1
    
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

    if counter_g % config["time_goon"] == 0:
        goon = random.choice(config["goon_messages"])

        # Prepare the message
        goon_message = goon["Text"]
        goon_image_url = goon["Image"]

        # Check if there's an image URL and append it to the message
        if goon_image_url:
            goon_message += f"\n{goon_image_url}"

        # Send the message to toad-tavern
        await goon_market_channel.send(message)
        counter_g = 0

@tipping.before_loop
async def before_tipping():
    logger.info("Waiting for bot to be ready...")
    await client.wait_until_ready()

if __name__ == "__main__":
    token = ""
    if not token:
        logger.critical("Token not found.")
        exit(1)
    try:
        client.run(token, log_handler=handler, log_formatter=formatter)
    except LoginFailure:
        logger.critical("Invalid token, restart the program.")
