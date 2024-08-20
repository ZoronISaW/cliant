import subprocess
import discord
from discord.client import aiohttp
from discord.ext import commands
import asyncio
import random
import string
import threading
import requests
import time
import json
import websockets
import sys
import re
import io
import datetime
import functools
import string
import urllib.parse
import urllib.request
import time
from urllib import parse, request
from itertools import cycle
import signal

running_threads = {}

PREFIX = ""

auto_responder_target_id = None
auto_pressure_target_id = None
user_reactions = {}
copied_messages = {}
active_countdowns = {}
layout_to_copy = {}
mimic_user = None
sending_task = None
stfu_messages = []
ass_messages = []
GCFLYPATH = "C:/Users/saban/Desktop/extra/slimemultitokengc.py" # alr so is the path for ur gc name changer file
helper_process = None   
HELPER_SCRIPT_PATH = "" # dis da auto press file



TOKEN = "OTQyOTYzNDE3NDAzMjM2MzUz.GFGycM.GOlm-r7oI3KyenvVV57Qh0rtqDTa243Ziv93t4"



should_flood_file = "should_flood.txt"
should_flood = False
try:
    with open(should_flood_file, "r") as file:
        should_flood = bool(file.read())
except FileNotFoundError:
    pass  # If the file doesn't exist, start with the default value (False)

# Function to update the should_flood state in the file
def update_should_flood(value):
    with open(should_flood_file, "w") as file:
        file.write(str(value))


GC_Name = [
"outlast me ", "slow fucking dork LOL ", "u cant beat me ", "i dont fold ", "hideous pedos ", "ur a fucking loser ", "dont fucking step ", "we going forever btw ", "lowtier punk ", "nigga got put down ",
]
Regular_Spammer_Message = [" @everyone die to me slut ", " @everyone outlast me then "]
gc_name_counter = 0
spam_counter = 0  # Initialize spam_counter
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="", self_bot=True, intents=intents)

@bot.command(name='mx')
async def change_group_name(ctx, *, new_name: str):
    await ctx.message.delete()
    number = 1
    channel_id = ctx.channel.id
    bot.loop_active = True
    while bot.loop_active:
        gc = bot.get_channel(channel_id)
        if isinstance(gc, discord.GroupChannel):
            name = f"{new_name} {number}"
            try:
                await gc.edit(name=name)
            except discord.HTTPException as e:
                if e.status == 503:
                    retry_count = getattr(ctx, 'retry_count', 0)
                    if retry_count < 3:
                        print("Service Unavailable, retrying...")
                        await asyncio.sleep(5)
                        ctx.retry_count = retry_count + 1
                        continue
                    else:
                        print("Service Unavailable, maximum retry attempts reached.")
                else:
                    raise e
            await asyncio.sleep(0.01)
            number += 1

@bot.command(name='quit')
async def stop_loop(ctx):
    bot.loop_active = False

def readtokens(filename='stored_tokens2.txt'):
    with open(filename, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

async def update_presence1(token, details):
    if token.strip() == "":
        print("Skipping empty token")
        return

    client = discord.Client()

    @client.event
    async def on_ready():
        activity = discord.Streaming(
            name=details,  # Use details as the status message
            url='https://www.twitch.tv/roblox'
        )
        await client.change_presence(activity=activity)

    try:
        await client.start(token, bot=False)  # bot=False specifies this is a user account token
    except discord.LoginFailure:
        print(f"Failed to login with token: {token} - Invalid token")
    except Exception as e:
        print(f"An error occurred with token: {token} - {e}")

async def streamall(ctx, messages):
    tokens = readtokens('stored_tokens2.txt')
    details = [random.choice(messages) for x in range(len(tokens))]

    tasks = [update_presence1(token, detail) for token, detail in zip(tokens, details)]
    await asyncio.gather(tasks)
    await ctx.send(f"Statuses updated for all tokens")


@bot.command()
async def sa(ctx,*, message: str):  # Use * to capture the entire message
    messages = message.split(', ')  # Split the input message into a list of messages
    await streamall(ctx, messages)     

@bot.command()
async def update_presence(details):
    """Update the custom status presence."""
    await bot.change_presence(activity=discord.Streaming(name=details, url='https://www.twitch.tv/roblox'))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    await update_presence("Welcome to my stream!")

@bot.command()
async def stream(ctx, *, message: str):
    """Change the custom status message."""
    await update_presence(message)
    await ctx.send(f"Streaming status updated to: {message}")
    await ctx.message.delete(2.5)
    

    
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

running_threads = {}
voice_tasks = {}

def Changer(channel_id):
    global gc_name_counter
    while not threading.current_thread().stopped():
        try:
            random_name = random.choice(GC_Name)
            response = requests.patch(
                f'https://discord.com/api/v9/channels/{channel_id}',
                headers={"Authorization": TOKEN},
                json={"name": f"{random_name} {gc_name_counter}"}
            )
            response.raise_for_status()
            gc_name_counter += 1
            time.sleep(0.07)  # Adjust the delay as needed
        except Exception as e:
            print(f"An error occurred in Changer: {e}")
            time.sleep(1)  # Retry after delay

def spam_messages(channel_id):
    global spam_counter  # Declare spam_counter as a global variable
    while not threading.current_thread().stopped():
        try:
            random_message = random.choice(Regular_Spammer_Message)
            response = requests.post(
                f"https://discordapp.com/api/v6/channels/{channel_id}/messages",
                headers={"Authorization": TOKEN},
                json={"content": f"{random_message}"}
            )
            response.raise_for_status()
            spam_counter += 1  # Increment spam_counter
            time.sleep(1)  # Adjust the delay between messages as needed
        except Exception as e:
            print(f"An error occurred in spam_messages: {e}")
            time.sleep(1)  # Retry after delay

async def connect_to_voice(channel_id, event):
    uri = 'wss://gateway.discord.gg/?v=9&encoding=json'
    while not event.is_set():
        try:
            async with websockets.connect(uri, max_size=None) as websocket:
                identify_payload = {
                    'op': 2,
                    'd': {
                        'token': TOKEN,
                        'intents': 513,
                        'properties': {
                            '$os': 'linux',
                            '$browser': 'my_library',
                            '$device': 'my_library'
                        }
                    }
                }
                identify_payload_str = json.dumps(identify_payload)
                await websocket.send(identify_payload_str)

                voice_state_payload = {
                    'op': 4,
                    'd': {
                        'guild_id': None,
                        'channel_id': channel_id,
                        'self_mute': False,
                        'self_deaf': False,
                        'self_video': False,
                        'request_to_speak_timestamp': round(time.time())
                    }
                }
                voice_state_payload_str = json.dumps(voice_state_payload)
                await websocket.send(voice_state_payload_str)

                voice_state_payload = {
                    'op': 4,
                    'd': {
                        'guild_id': None,
                        'channel_id': None,
                        'self_mute': False,
                        'self_deaf': False,
                        'self_video': False
                    }
                }
                voice_state_payload_str = json.dumps(voice_state_payload)
                await websocket.send(voice_state_payload_str)

                url = f'https://discord.com/api/v9/channels/{channel_id}/call/ring'
                headers = {
                    'Authorization': f'{TOKEN}',
                    'User-Agent': 'my_library/0.0.1',
                    'Content-Type': 'application/json'
                }
                data = {'recipients': None}
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 204:
                    print("Successfully notified GC.")
                else:
                    print(f'Failed to notify GC with status code {response.status_code}')
        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(1)  # Retry after delay

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

@bot.command()
async def gc(ctx, gc_id: int):
    if gc_id in running_threads:
        await ctx.send(f"Actions are already running in GC {gc_id}. Use !gc_end {gc_id} to stop them first.")
        return

    changer_thread = StoppableThread(target=Changer, args=(gc_id,))
    spam_thread = StoppableThread(target=spam_messages, args=(gc_id,))
    voice_event = asyncio.Event()

    running_threads[gc_id] = [changer_thread, spam_thread]
    voice_tasks[gc_id] = voice_event

    changer_thread.start()
    spam_thread.start()

    await ctx.send(f"Starting actions in GC {gc_id}.")
    await connect_to_voice(gc_id, voice_event)

@bot.command()
async def gc_end(ctx, gc_id: int):
    if gc_id not in running_threads:
        await ctx.send(f"No actions running in GC {gc_id}.")
        return

    threads = running_threads.pop(gc_id)
    for thread in threads:
        thread.stop()
        thread.join()

    if gc_id in voice_tasks:
        voice_tasks[gc_id].set()
        voice_tasks.pop(gc_id)

    await ctx.send(f"discord.gg/chatpacking")

counter = 0
counter2 = 0
counter_file = "counter.txt"
hail_task = None
hail_sentences = [
"WEAK ASS QUEER BITCH <@{target}>",
"SOFT\nASS\nASS\nNIGGA\nSHUT\nTHE\nFUCK\nUP <@{target}>",
"USELESS\nASS\nDIRTY\nCUTSLUT\nDIE\nWHORE <@{target}>",
"SOFT ASS FAGGOT PEDOPHILE <@{target}>",
"FRAIL BIG NECK HOMOSEXUAL BISON <@{target}>",
"U\nSUCK\nCRAZY\nASS\nNIGGA\nSILENCE\nDIRTY\nASS\nPEDOPHILE\nWE\nDONT\nSUPPORT\nYOU <@{target}>",
"BEG ME FOR MERCY <@{target}>",
"GET UR SKULL SMASHED WEAKLING <@{target}>",
"NASTY\nFAT\nNECK\nDISGUSTING\nANIMAL\nMOLESTOR <@{target}>",
"SHUT UR SHITTY ASS UP <@{target}>",
"I\nJUST\nSTOLE\nYO\nKNEECAPS\nSOFT\nBITCH\nCRAWL\nAWAY <@{target}>",
"<@{target}> STOP EATING RAW SHIT",
"DISGUSTING\nOGRE\n3\nHEADS\nVOMIT\nBREATING\nAPE <@{target}>",
"NIGGA YOU SUCK LOL <@{target}>",
"YOU DISGUSTING WASTE OF OXYGEN <@{target}>",
"UR\nUSELESS\nAS\nSHIT\nKILL\nYOURSELF\nLMAO <@{target}>",
"UR NOT ON MY LEVEL PEASENT <@{target}>",
"HOBO ASS NIGGA <@{target}>",
"YOULL\nNEVER\nBE\nAS\nGOOD\nAS\nME <@{target}>"
"COME GET UR SKIN PIERCED <@{target}>",
"CRY BITCH IM NOT STOPPING <@{target}>",
"DOGSHIT ASS NIGGA <@{target}>",
"LOL UR ASS <@{target}>",
"YO\nCUTSLUT\nCARVE\nUR\nSKIN\nTO\nSHREDS\nU\nSHITTY\nHUMAN\nBEING\nYOU\nSERVE\nNO\nPURPOSE <@{target}>",
"WAH WAH NIGGA YOU SUCK STFU <@{target}>",
"ILL\nPIERCE\nYOUR\nFUCKING\nEYEBALLS\nAND\nTURN\nTHEM\nTO\nSHREDS\nYOU\nWEAK\nPEDOPHILE\nFUCK <@{target}>",
"ANTISOICAL\nANOREXIC\nGOBLIN\nYOU\nEAT\nSHIT\nFOR\nBREAKFAST <@{target}>",
"YO FAT NECK ASS NIGGA STFU <@{target}>",
"STOP BREATHING AND LYNCH URSELF <@{target}>",
"I\nOWN\nYOU\nLMFAO\nWORTHLESS\nPIECE\nOF\nHOMOSAPIEN\nSEWAGE\nSHUT\nUR\nBIG\nNOSE\nASS\nUP <@{target}>",
"HAHAHA YOU SUCK NIGGA LMFAOOO <@{target}>",
]

auto_responses = [
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck dogshit ass nigga",
"SHUT\nUP\nFAGGOT\nASS\nNIGGA\nYOU\nARE\nNOT\nON\nMY\nLEVEL\nILL\nFUCKING\nKILL\nYOU\nDIRTY\nASS\nPIG\nBASTARD\nBARREL\nNOSTRIL\nFAGGOT\nI\nOWN\nYOU\nKID\nSTFU\nLAME\nASS\nNIGGA\nU\nFUCKING\nSUCK\nI\nOWN\nBOW\nDOWN\nTO\nME\nPEASENT\nFAT\nASS\nNIGGA",
"ILL\nTAKE\nUR\nFUCKING\nSKULL\nAND\nSMASH\nIT\nU\nDIRTY\nPEDOPHILE\nGET\nUR\nHANDS\nOFF\nTHOSE\nLITTLE\nKIDS\nNASTY\nASS\nNIGGA\nILL\nFUCKNG\nKILL\nYOU\nWEIRD\nASS\nSHITTER\nDIRTFACE\nUR\nNOT\nON\nMY\nLEVEL\nCRAZY\nASS\nNIGGA\nSHUT\nTHE\nFUCK\nUP",
"NIGGAS\nTOSS\nU\nAROUND\nFOR\nFUN\nU\nFAT\nFUCK\nSTOP\nPICKING\nUR\nNOSE\nFAGGOT\nILL\nSHOOT\nUR\nFLESH\nTHEN\nFEED\nUR\nDEAD\nCORPSE\nTO\nMY\nDOGS\nU\nNASTY\nIMBECILE\nSTOP\nFUCKING\nTALKING\nIM\nABOVE\nU\nIN\nEVERY\nWAY\nLMAO\nSTFU\nFAT\nNECK\nASS\nNIGGA",
"dirty ass rodent molester",
"ILL\nBREAK\nYOUR\nFRAGILE\nLEGS\nSOFT\nFUCK\nAND\nTHEN\nSTOMP\nON\nUR\nDEAD\nCORPSE",
"weak prostitute",
"stfu dork ass nigga",
"garbage ass slut",
"ur weak",
"why am i so above u rn",
"soft ass nigga",
"frail slut",
"ur slow as fuck",
"ILL\nPIERCE\nUR\nFUCKING\nVEINS\nU\nDOGSHIT\nFAGGOT\nUR\nNOT\nON\nMY\nLEVEL",
"you cant beat me",
"shut the fuck up LOL",
"you suck faggot ass nigga be quiet",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck faggot ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck weak ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck soft ass nigga",
"YOU SUCK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nwtf\nyoure\nslow\nas\nfuck\nlmao\nSHUT\nTHE\nFUCK\nUP\nLMFAOO\nyou suck hoe ass nigga",
]


auto_responses_enabled = True
auto_adder_enabled = False
auto_adder_thread = None
user_id_to_add = None

try:
    with open(counter_file, "r") as file:
        counter =   int(file.read())
except FileNotFoundError:
    pass  # If the file doesn't exist, start with the default counter value (0)

# AutoAdder function
def AutoAdder(user_id, gc_id):
    global user_id_to_add
    while auto_adder_enabled:
        time.sleep(0.00001)
        try:
            r = requests.get(
                f'https://discord.com/api/v9/channels/{gc_id}',
                headers={'Authorization': TOKEN}
            )

            print(r.status_code)
            data = r.json()
            recipients = data['recipients']

            for i, x in enumerate(recipients):
                userid = x['id']

                if userid == user_id:
                    print("User is in GC.")
                    print(userid)
                    break

            else:
                if len(recipients) - 1 == i:
                    print("user not in gc")

                    add = requests.put(
                        f'https://discord.com/api/v9/channels/{gc_id}/recipients/{user_id}',
                        headers={'Authorization': TOKEN}
                    )

                else:
                    print(i)
                    continue

        except Exception as e:
            print(f"An error occurred in AutoAdder: {e}")

# Function to start the thread
def run_threads(user_id, gc_id):
    global auto_adder_thread, auto_adder_enabled
    auto_adder_enabled = True
    auto_adder_thread = threading.Thread(target=AutoAdder, args=(user_id, gc_id))
    auto_adder_thread.start() 

# Function to stop the thread
def stop_threads():
    global auto_adder_thread, auto_adder_enabled
    auto_adder_enabled = False
    if auto_adder_thread and auto_adder_thread.is_alive():
        auto_adder_thread.join()


# Discord bot events and commands
@bot.event
async def on_ready():
    print(f" ** Logged in as: {bot.user.name} **")
    print("Use 'victim respID pressID' to set the victim user IDs.")
    print("!Menu for all commands u stupid faggots - slime")

# Command to set victim users for auto-responder and auto-pressure functionalities
@bot.command()
async def r(ctx, auto_responder: discord.User):
    try:
        # Set the global variables to the IDs of the mentioned users
        global auto_responder_target_id
        auto_responder_target_id = auto_responder.id
        

        # Print out the mentions for debugging
        auto_responder_mention = auto_responder.mention
        
        print(f"Auto-responder mention: {auto_responder_mention}")
        await asyncio.sleep(1)
        # Send a confirmation message
        confirmation_msg = await ctx.send("👍")

        # Delete the confirmation message after 1 second
        await asyncio.sleep(1)
        await confirmation_msg.delete()

        # Delete the command message after 1 second
        await asyncio.sleep(1)
        await ctx.message.delete()

    except Exception as e:
        print(f"An error occurred in 'victim' command: {e}")
        await ctx.send("An error occurred while setting victim IDs.")

@bot.command()
async def p(ctx, auto_pressure: discord.User):
    try:
        # Set the global variables to the IDs of the mentioned users
        global auto_pressure_target_id
        auto_pressure_target_id = auto_pressure.id

        # Print out the mentions for debugging
        auto_pressure_mention = auto_pressure.mention
        print(f"Auto-pressure mention: {auto_pressure_mention}")
        await asyncio.sleep(1)
        # Send a confirmation message
        confirmation_msg = await ctx.send("👍")

        # Delete the confirmation message after 1 second
        await asyncio.sleep(1)
        await confirmation_msg.delete()

        # Delete the command message after 1 second
        await asyncio.sleep(1)
        await ctx.message.delete()

    except Exception as e:
        print(f"An error occurred in 'victim' command: {e}")
        await ctx.send("An error occurred while setting victim IDs.")


# Command to check the bot's status
@bot.command()
async def check(ctx):
    msg = await ctx.send("**Zoron > you slut.**")
    await asyncio.sleep(2)
    await msg.delete()
    await ctx.message.delete()

# Command to spam messages in the current channel
@bot.command()
async def spam(ctx, *, args):
    args_list = args.split()

    if len(args_list) < 3:
        msg = await ctx.send("Please provide the message, count, and delay.")
        await asyncio.sleep(2)
        await msg.delete()
        return

    message = " ".join(args_list[:-2])
    count = int(args_list[-2])
    delay = float(args_list[-1])

    sent_messages = 0
    for i in range(count):
        sent_messages += 1
        print(f"Message '{message}' sent {sent_messages}/{count}")
        await ctx.send(message)
        await asyncio.sleep(delay)

    await asyncio.sleep(0.0000000000000000000000000000000000012)
    await ctx.message.delete()

# Command to start sending 'hail' messages with an optional delay
@bot.command()
async def killer(ctx, delay: int = 0):
    global hail_task
    global counter2

    if hail_task is None:
        counter2 += 1
        hail_task = asyncio.create_task(send_hail_sentences(ctx, delay))
    await asyncio.sleep(2)
    await ctx.message.delete()

# Command to disable auto-pressure
@bot.command()
async def end1(ctx):
    global hail_task
    global counter

    if hail_task is not None and not hail_task.done():
        hail_task.cancel()
        hail_task = None
        counter += 1
        
        msg2 = await ctx.send(f" **You are ZORON'S victim #{counter} **")
        await asyncio.sleep(2)
        
        await msg2.delete()
        await ctx.message.delete()

        # Save the updated counter value to the file
        with open(counter_file, "w") as file:
            file.write(str(counter))

# Function to send 'hail' sentences with a delay
async def send_hail_sentences(ctx, delay):
    while True:
        sentence = random.choice(hail_sentences)
        sentence_with_target = sentence.format(target=auto_pressure_target_id)
        await ctx.send(sentence_with_target)
        await asyncio.sleep(delay)

# Command to disable auto-responses
@bot.command()
async def end(ctx):
    global auto_responses_enabled
    auto_responses_enabled = False
    
    await asyncio.sleep(2)
   
    await ctx.message.delete()

# Command to enable auto-responses
@bot.command()
async def start(ctx):
    global auto_responses_enabled
    auto_responses_enabled = True
    
    await asyncio.sleep(2)
    
    await ctx.message.delete()

# Command to start sending 'hail' messages with a specified delay
@bot.command()
async def start1(ctx, delay: int):
    global hail_task
    if delay <= 0:
        msg = await ctx.send(" **Delay must be a positive integer.** ")
        await asyncio.sleep(2)
        await msg.delete()
        await ctx.message.delete()
        return
    
    if hail_task is not None and not hail_task.done():
        hail_task.cancel()

    msg = await ctx.send(f" **Auto-Pressure enabled with a {delay} second delay.**")
    await asyncio.sleep(2)
    await msg.delete()
    await ctx.message.delete()
    hail_task = asyncio.create_task(send_hail_sentences(ctx, delay))

# Command to change the delay between 'hail' messages
@bot.command()
async def change(ctx, delay: int):
    global hail_task
    if delay <= 0:
        msg = await ctx.send(" **Delay must be a positive integer.** ")
        await asyncio.sleep(2)
        await msg.delete()
        await ctx.message.delete()
        return
    
    if hail_task is not None and not hail_task.done():
        hail_task.cancel()

    msg = await ctx.send(f" ** messages will now be sent with a {delay} second delay.** ")
    await asyncio.sleep(2)
    await msg.delete()
    await ctx.message.delete()
    hail_task = asyncio.create_task(send_hail_sentences(ctx, delay))



@bot.command()
async def purge(ctx, user_id: int):
    # Try to fetch the user by ID
    user = bot.get_user(user_id)
    if not user:
        await ctx.send("User not found.")
        return
    
    # Try to create a DM channel with the user
    dm_channel = await user.create_dm()
    if not dm_channel:
        await ctx.send("Could not create a DM channel with the specified user.")
        return

    # Counter to keep track of deleted messages
    deleted_count = 0

    # Loop through the history of the DM channel
    async for message in dm_channel.history(limit=None):  # Adjust the limit if necessary
        if message.author == bot.user:  # Checks if the message is sent by the bot
            await message.delete()
            deleted_count += 1
            await asyncio.sleep(0.000000000000001)  # Sleep to respect rate limits, adjust as necessary

    await ctx.send(f"Purged {deleted_count} messages from DMs with {user.display_name}.", delete_after=5)  # Notification message




# Command to prevent a user from leaving a group chat
@bot.command()
async def noleave(ctx, user: discord.User, gc_id: int):
    global user_id_to_add
    user_id_to_add = user.id
    run_threads(user.id, gc_id)
    await ctx.message.delete()

# Command to stop preventing the specified user from leaving the group chat
@bot.command()
async def end2(ctx):
    stop_threads()
    await ctx.message.delete()

# Command to change the user ID for preventing leaving a group chat
@bot.command()
async def change1(ctx, new_user: discord.User):
    global user_id_to_add
    user_id_to_add = new_user.id
    await ctx.message.delete()

# Command to send a message to all friends through DM
@bot.command()
async def massdm(ctx, *, message: str):
    for user in bot.user.friends:
        try:
            await user.send(message)
            print(f"messaged: {user.name}")
        except:
            print(f"couldn't message: {user.name}")

# Command to display the command menu
@bot.command()
async def menu(ctx):
   
    menu_text = "```yaml\n \nCommand Menu:\n\n"
    menu_text += "!gc [gc_id]: Perform actions in the specified GC associated with the provided GC ID.\n"
    menu_text += "!victim [auto_responder] [auto_pressure]: Set victim IDs for auto-responder and auto-pressure functionalities.\n"
    menu_text += "!check: Check the bot's status.\n"
    menu_text += "1hail [delay]: Start sending 'hail' messages with an optional delay between messages.\n"
    menu_text += "!end1: Disable auto-pressure.\n"
    menu_text += "!start: Enable auto-responses.\n"
    menu_text += "!purge [amount]: Delete a certain number of messages from the current channel.\n"
    menu_text += "!start1 [delay]: Start sending 'hail' messages with a specified delay between messages.\n"
    menu_text += "!change [delay]: Change the delay between 'hail' messages.\n"
    menu_text += "!noleave [user] [gc_id]: Prevent a user from leaving a group chat.\n"
    menu_text += "!end2: Stop preventing the specified user from leaving the group chat.\n"
    menu_text += "!massdm [message]: Send a message to all your friends through DM.\n"
    menu_text += "!react [user] [emoji]: React to messages from the specified user with the specified emoji.\n"
    menu_text += "!reactend [user]: Stop reacting to messages from the specified user.\n"
    menu_text +="!rape: rape [user] to rape them.\n"
    menu_text +="!Known: Known [user] to determine how known they are based on your mutuals.\n"
    menu_text+="!Afkcheck: afkcheck @user to count afk check till 100.\n"
    menu_text += "!Cum Masturbate on niggas ( so disrespectul) We gon do weird shit to you ;).\n"
    menu_text += "!Hack [user]: It doxxes niggas They gonna get depressed.\n"
    menu_text += "!911 KABOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOM: \n"
    menu_text += "!Tweet [user]: TWEETS PEOPLE \n "
    menu_text += "**This Does Not Go Against Discord Tos!**"
    menu_text += "```**Made By Zoron**```"
    menu_message = await ctx.send(menu_text, delete_after=1001010110101010101010010101)  # Self-delete after 1001010110101010101010010101 seconds






@bot.command()
async def changer(ctx, channel_id: int):
    global gc_name_counter
    try:
        while True:
            for _ in range(5):
                random_name = random.choice(GC_Name)
                response = requests.patch(
                    f'https://discord.com/api/v9/channels/{channel_id}',
                    headers={"Authorization": TOKEN},
                    json={"name": f"{random_name} {gc_name_counter}"}
                )
                response.raise_for_status()
                print(f"Changed GC name to: {random_name}")
                gc_name_counter += 1
                await asyncio.sleep(1)  # Add a short delay between each name change

            # Take a break for 5 seconds
            print("Taking a break for 5 seconds...")
            await asyncio.sleep(5)

    except Exception as e:
        print(f"An error occurred in Changer: {e}")




# Command to set reaction for a user
@bot.command()
async def react(ctx, user: discord.User, emoji: str):
    # Add or update the user's reaction in the dictionary
    user_reactions[user.id] = emoji

# Command to remove reaction for a user
@bot.command()
async def reactend(ctx, user: discord.User):
    # Check if the user ID exists in the dictionary
    if user.id in user_reactions:
        # Remove the user ID from the dictionary
        del user_reactions[user.id]
    else:
        await ctx.send(f"No reaction set for user {user.name}")





@bot.command()
async def afkcheck(ctx, user: discord.User):
    countdown = 100

    # Countdown loop
    while countdown >= 0:
        await ctx.send(f"# afkcheck son: {countdown}")
        countdown -= 1

        # Check if the user has sent a message
        async for message in ctx.channel.history(limit=1):
            if message.author == user:
                await ctx.send(f"# {user.display_name} WELCOME BACK SONNY")
                return
        await asyncio.sleep(2)

    await ctx.send(f"# {user.display_name} NICE FOLD LOL")



    


@bot.event
async def on_message(message):
    
 


    # Check if the message is from a user with a specified reaction
    if message.author.id in user_reactions:
        # React to the message with the specified emoji
        emoji = user_reactions[message.author.id]
        await message.add_reaction(emoji)
    
    # Check if auto-responses are enabled and the message is from the auto-responder target
    if auto_responses_enabled and message.author.id == auto_responder_target_id:

        # Select a random auto-response and send it
        response = random.choice(auto_responses)
        await message.reply(response)
        # You can also add reactions here if needed
    if message.author.id in copied_messages:
        # Send the copied message using the bot
        await message.channel.send(copied_messages[message.author.id])
    # Continue processing other commands and events
        
    global mimic_user
    if mimic_user and message.author == mimic_user:
        await message.channel.send(message.content)
    
    
    
    
    
     # Check if the message author was in the active countdowns
    if message.author in active_countdowns:
        # Remove the user from active countdowns
        del active_countdowns[message.author]
        await message.channel.send(f"The AFK check for {message.author.display_name} has been canceled.")

    await bot.process_commands(message)




# Command to get the avatar of a user
@bot.command()
async def av(ctx, user: discord.User = None):
    try:
        if user is None:  # If no user is provided, get the bot's own avatar
            user = bot.user

        # Check if the user has an avatar
        if user.avatar:
            avatar_url = user.avatar_url
            await ctx.send(f"Avatar URL: {avatar_url}", delete_after=10101010101001010100101111)  # Delete response message after 10101010101001010100101111 seconds
        else:
            await ctx.send(f"{user.name} does not have an avatar.", delete_after=10101010101001010100101111)  # Delete response message after 10101010101001010100101111 seconds

        # Delete the command message itself after 2 seconds
        await asyncio.sleep(2)
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"An error occurred: {e}", delete_after=10101010101001010100101111)  # Delete response message after 10101010101001010100101111 seconds




@bot.command()
async def known(ctx, user: discord.User):
    await ctx.send(f"How many mutuals does dis ugly nigga have? ")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel and message.content.isdigit() and 1 <= int(message.content) <= 10

    try:
        response = await bot.wait_for('message', check=check, timeout=60)  # Wait for user's response for up to 60 seconds
        mutuals = int(response.content)
        known_percentage = random.randint(mutuals * 10, mutuals * 10 + 10)  # Each mutual increases the known percentage by 10%
        
        if known_percentage < 50:
            known_status = "Unknown"
        elif known_percentage == 50:
            known_status = "Somewhat known"
        else:
            known_status = "Known"

        await ctx.send(f"# this hideous nigga name {user.name} is {known_percentage}% known ({known_status})")
    except asyncio.TimeoutError:
        await ctx.send("u took too long to respond bum nigga")
    except ValueError:
        await ctx.send("1-10 nga")

edit_messages = [
    "**Unzips dick**",
    "**Puts it in your mouth**",
    "**Aggresivly pulls your hair knowing you dont like it **:smiling_imp: :smiling_imp: ",
    "**Starts going harder while seeing you choking**",
    "Ohh im about to cum:sweat_drops: :sweat_drops: ",
    "**Fills your mouth with my cum**",
    "Goodboy.:heart::heart:"
]        
    
@bot.command()
async def rape(ctx, user: discord.User):
    # Send the initial message with a mention to the user
    message = await ctx.send(f"{user.mention}, YOU ARE GETTING RAPED LOL")

    # Edit the message 7 times
    for i in range(7):
        await asyncio.sleep(1)  # Delay for 1 second (adjust as needed)
        edit_content = edit_messages[i % len(edit_messages)]
        await message.edit(content=f"{user.mention}, {edit_content}")

@bot.command()
async def kiss(ctx, user: discord.User):
    await ctx.message.delete()
    r = requests.get("https://nekos.life/api/v2/img/kiss")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention, file=discord.File(file, f"exeter_kiss.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)

@bot.command(aliases=["9/11", "911", "terrorist"])
async def nine_eleven(ctx):
    await ctx.message.delete()
    invis = ""  # char(173)
    message = await ctx.send(f'''
{invis}:man_wearing_turban::airplane:    :office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis} :man_wearing_turban::airplane:   :office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis}  :man_wearing_turban::airplane:  :office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis}   :man_wearing_turban::airplane: :office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content=f'''
{invis}    :man_wearing_turban::airplane::office:           
''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
        :boom::boom::boom:    
        ''')
@bot.command(aliases=["jerkoff", "ejaculate", "orgasm"])
async def cum(ctx):
    await ctx.message.delete()
    message = await ctx.send('''
            :ok_hand:            :smile:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :smiley:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:  
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :grimacing:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant:  
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :persevere:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:   
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                      :ok_hand:            :confounded:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:=D 
             :trumpet:      :eggplant: 
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :tired_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D 
             :trumpet:      :eggplant:    
             ''')
    await asyncio.sleep(0.5)
    await message.edit(contnet='''
                       :ok_hand:            :weary:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8=:punch:= D:sweat_drops:
             :trumpet:      :eggplant:        
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :dizzy_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')
    await asyncio.sleep(0.5)
    await message.edit(content='''
                       :ok_hand:            :drooling_face:
   :eggplant: :zzz: :necktie: :eggplant: 
                   :oil:     :nose:
                 :zap: 8==:punch:D :sweat_drops:
             :trumpet:      :eggplant:                 :sweat_drops:
     ''')





@bot.command()
async def tweet(ctx, username: str = None, *, message: str = None):
    await ctx.message.delete()
    if username is None or message is None:
        await ctx.send("missing parameters")
        return
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}") as r:
            res = await r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"exeter_tweet.png"))
            except:
                await ctx.send(res['message'])


@bot.command()
async def hack(ctx, user: discord.Member = None):
    await ctx.message.delete()
    gender = ["Male", "Female", "Trans", "Other", "Retard"]
    age = str(random.randrange(10, 25))
    height = ['4\'6\"', '4\'7\"', '4\'8\"', '4\'9\"', '4\'10\"', '4\'11\"', '5\'0\"', '5\'1\"', '5\'2\"', '5\'3\"',
              '5\'4\"', '5\'5\"',
              '5\'6\"', '5\'7\"', '5\'8\"', '5\'9\"', '5\'10\"', '5\'11\"', '6\'0\"', '6\'1\"', '6\'2\"', '6\'3\"',
              '6\'4\"', '6\'5\"',
              '6\'6\"', '6\'7\"', '6\'8\"', '6\'9\"', '6\'10\"', '6\'11\"']
    weight = str(random.randrange(60, 300))
    hair_color = ["Black", "Brown", "Blonde", "White", "Gray", "Red"]
    skin_color = ["White", "Pale", "Brown", "Black", "Light-Skin"]
    religion = ["Christian", "Muslim", "Atheist", "Hindu", "Buddhist", "Jewish"]
    sexuality = ["Straight", "Gay", "Homo", "Bi", "Bi-Sexual", "Lesbian", "Pansexual"]
    education = ["High School", "College", "Middle School", "Elementary School", "Pre School",
                 "Retard never went to school LOL"]
    ethnicity = ["White", "African American", "Asian", "Latino", "Latina", "American", "Mexican", "Korean", "Chinese",
                 "Arab", "Italian", "Puerto Rican", "Non-Hispanic", "Russian", "Canadian", "European", "Indian"]
    occupation = ["Retard has no job LOL", "Certified discord retard", "Janitor", "Police Officer", "Teacher",
                  "Cashier", "Clerk", "Waiter", "Waitress", "Grocery Bagger", "Retailer", "Sales-Person", "Artist",
                  "Singer", "Rapper", "Trapper", "Discord Thug", "Gangster", "Discord Packer", "Mechanic", "Carpenter",
                  "Electrician", "Lawyer", "Doctor", "Programmer", "Software Engineer", "Scientist"]
    salary = ["Retard makes no money LOL", "$" + str(random.randrange(0, 1000)), '<$50,000', '<$75,000', "$100,000",
              "$125,000", "$150,000", "$175,000",
              "$200,000+"]
    location = ["Retard lives in his mom's basement LOL", "America", "United States", "Europe", "Poland", "Mexico",
                "Russia", "Pakistan", "India",
                "Some random third world country", "Canada", "Alabama", "Alaska", "Arizona", "Arkansas", "California",
                "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana",
                "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
                "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
                "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
                "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
                "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    email = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com", "@protonmail.com", "@disposablemail.com",
             "@aol.com", "@edu.com", "@icloud.com", "@gmx.net", "@yandex.com"]
    dob = f'{random.randrange(1, 13)}/{random.randrange(1, 32)}/{random.randrange(1950, 2021)}'
    name = ['James Smith', "Michael Smith", "Robert Smith", "Maria Garcia", "David Smith", "Maria Rodriguez",
            "Mary Smith", "Maria Hernandez", "Maria Martinez", "James Johnson", "Catherine Smoaks", "Cindi Emerick",
            "Trudie Peasley", "Josie Dowler", "Jefferey Amon", "Kyung Kernan", "Lola Barreiro",
            "Barabara Nuss", "Lien Barmore", "Donnell Kuhlmann", "Geoffrey Torre", "Allan Craft",
            "Elvira Lucien", "Jeanelle Orem", "Shantelle Lige", "Chassidy Reinhardt", "Adam Delange",
            "Anabel Rini", "Delbert Kruse", "Celeste Baumeister", "Jon Flanary", "Danette Uhler", "Xochitl Parton",
            "Derek Hetrick", "Chasity Hedge", "Antonia Gonsoulin", "Tod Kinkead", "Chastity Lazar", "Jazmin Aumick",
            "Janet Slusser", "Junita Cagle", "Stepanie Blandford", "Lang Schaff", "Kaila Bier", "Ezra Battey",
            "Bart Maddux", "Shiloh Raulston", "Carrie Kimber", "Zack Polite", "Marni Larson", "Justa Spear"]
    phone = f'({random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)})-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}'
    if user is None:
        user = ctx.author
        password = ['password', '123', 'mypasswordispassword', user.name + "iscool123", user.name + "isdaddy",
                    "daddy" + user.name, "ilovediscord", "i<3discord", "furryporn456", "secret", "123456789", "apple49",
                    "redskins32", "princess", "dragon", "password1", "1q2w3e4r", "ilovefurries"]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into this nigga life...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into this nigga life...\nCaching data...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into this nigga life...\nCaching data...\nCracking SSN information...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into this nigga life...\nCaching data...\nCracking SSN information...\ncalling his momma love life details...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into this nigga life...\nCaching data...\nCracking SSN information...\ncallin his momma...\nFinalizing life-span dox details\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"```Successfully hacked {user}\nName: {random.choice(name)}\nGender: {random.choice(gender)}\nAge: {age}\nHeight: {random.choice(height)}\nWeight: {weight}\nHair Color: {random.choice(hair_color)}\nSkin Color: {random.choice(skin_color)}\nDOB: {dob}\nLocation: {random.choice(location)}\nPhone: {phone}\nE-Mail: {user.name + random.choice(email)}\nPasswords: {random.choices(password, k=3)}\nOccupation: {random.choice(occupation)}\nAnnual Salary: {random.choice(salary)}\nEthnicity: {random.choice(ethnicity)}\nReligion: {random.choice(religion)}\nSexuality: {random.choice(sexuality)}\nEducation: {random.choice(education)}```")
    else:
        password = ['password', '123', 'mypasswordispassword', user.name + "iscool123", user.name + "isdaddy",
                    "daddy" + user.name, "ilovediscord", "i<3discord", "furryporn456", "secret", "123456789", "apple49",
                    "redskins32", "princess", "dragon", "password1", "1q2w3e4r", "ilovefurries"]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into this nigga life...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into this nigga life...\nInfecting with The heroin deadly virus...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into this nigga life...\ninfecting with Heroin virus...\nspraying knocked nipple juice...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into this nigga life...\ninfecting with Heroin virus...\nspraying knocked nipple juice...\n callin his momma...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into this nigga life...\ninfecting with Heroin virus...\nspraying knocked nipple juice...\ncallin his momma...\nFinalizing life-span details\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"```Successfully hacked {user}\nName: {random.choice(name)}\nGender: {random.choice(gender)}\nAge: {age}\nHeight: {random.choice(height)}\nWeight: {weight}\nHair Color: {random.choice(hair_color)}\nSkin Color: {random.choice(skin_color)}\nDOB: {dob}\nLocation: {random.choice(location)}\nPhone: {phone}\nE-Mail: {user.name + random.choice(email)}\nPasswords: {random.choices(password, k=3)}\nOccupation: {random.choice(occupation)}\nAnnual Salary: {random.choice(salary)}\nEthnicity: {random.choice(ethnicity)}\nReligion: {random.choice(religion)}\nSexuality: {random.choice(sexuality)}\nEducation: {random.choice(education)}```")
       


@bot.command(name='stfu')
async def stfu(ctx):
    global sending_task

    async def send_messages():
        for msg in stfu_messages:
            await ctx.send(f'{msg}')
            await asyncio.sleep(0.001)  # Adjust the sleep interval as needed

    if sending_task is not None:
        sending_task.cancel()

    sending_task = bot.loop.create_task(send_messages())

@bot.command(name='5')
async def five(ctx):
    await ctx.message.delete()
    global sending_task
    if sending_task is not None:
        sending_task.cancel()
        sending_task = None

@bot.command(name='ASS')
async def ass(ctx):
    global sending_task

    async def send_messages():
        for msg in ass_messages:
            await ctx.send(f'{msg}')
            await asyncio.sleep(0.000000000000000000000000000000000000000000000000000000012)  # Adjust the sleep interval as needed

    if sending_task is not None:
        sending_task.cancel()

    sending_task = bot.loop.create_task(send_messages())

@bot.command(name='stfu1')
async def stfu1(ctx, *, message):
    global stfu_messages
    stfu_messages = [msg.strip() for msg in message.split(',')]
    await ctx.send(f'Messages stored for stfu: {", ".join(stfu_messages)}')

@bot.command(name='ass1')
async def ass1(ctx, *, message):
    global ass_messages
    ass_messages = [msg.strip() for msg in message.split(',')]
    await ctx.send(f'Messages stored for ass: {", ".join(ass_messages)}')


@bot.command()
async def gang(ctx, channel_id: int):
    # Launch the helper bot script and pass the channel ID
    subprocess.Popen(["python", "C:/Users/user/Desktop/Other/Coding stuff/God bot/gr.py", str(channel_id)])
    

@bot.command()
async def gcfly(ctx, channel_id: int, counter: int, *names: str):
    global helper_process
    if helper_process is None:
        names_str = ','.join(names)
        helper_process = subprocess.Popen(["python", GCFLYPATH, str(channel_id), str(counter), names_str])
      

@bot.command()
async def gcflyend(ctx):
    global helper_process
    if helper_process is not None:
        helper_process.send_signal(signal.SIGTERM)
        helper_process = None
        await ctx.send(f"Stopped changing group chat names!")
    else:
        await ctx.send("No group chat name changer is running!")

@bot.command()
async def tap(ctx, user: discord.User, channel_id: int, *, messages: str):
    global helper_process
    if helper_process is None:
        helper_process = subprocess.Popen(["python", HELPER_SCRIPT_PATH, str(user.id), str(channel_id), messages])
        await ctx.send(f"Started spamming messages to {user.mention} in channel {channel_id} with messages: {messages}!")
    else:
        await ctx.send("Spamming process is already running!")

@bot.command()
async def tapend(ctx):
    global helper_process
    if helper_process is not None:
        helper_process.send_signal(signal.SIGTERM)
        helper_process = None
        await ctx.send("Stopped spamming process!")
    else:
        await ctx.send("No spamming process is currently running.")

        



@bot.command(aliases=["pornhubcomment", 'phc'])
async def phcomment(ctx, user: discord.User = None, *, args=None):
    await ctx.message.delete()
    if user is None or args is None:
        await ctx.send(f'[ERROR]: Invalid input! Command: phcomment <user> <message>')
        return

    # Use the mentioned user's avatar URL
    avatar_url = user.avatar_url_as(format="png")

    endpoint = f"https://nekobot.xyz/api/imagegen?type=phcomment&text={args}&username={user.name}&image={avatar_url}"
    r = requests.get(endpoint)
    res = r.json()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res["message"]) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"{user.name}_pornhub_comment.png"))
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@bot.command()
async def outlast(ctx, user: discord.User):
    countdown = 10000000000000000000

    # Countdown loop
    while countdown >= 0:
        await ctx.send(f"# lets outlast fag boy: {countdown} {user.id}")
        countdown -= 1

        # Check if the user has sent a message
        async for message in ctx.channel.history(limit=1):
            if message.author == user:
                await ctx.send(f"# {user.display_name} WELCOME BACK SONNY")
                return
        await asyncio.sleep(2)

    await ctx.send(f"# {user.display_name} NICE FOLD LOL")
    

GC_Name1 = [
    "YOU ASS SON PATTERN UP ", " DO SUM BOUT IT PUSSY LOL", "UGLY HIDEOUS CUCK FOLD TO ME"
]

gc_name_counter = 0

intents = discord.Intents.default()
intents.members = True


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

running_threads = {}

def Changers(channel_id):
    global gc_name_counter
    while not threading.current_thread().stopped():
        try:
            random_name = random.choice(GC_Name)
            response = requests.patch(
                f'https://discord.com/api/v9/channels/{channel_id}',
                headers={"Authorization": TOKEN},
                json={"name": f"{random_name} {gc_name_counter}"}
            )
            response.raise_for_status()
            gc_name_counter += 1
            time.sleep(0.1)  # Adjust the delay as needed
        except Exception as e:
            print(f"An error occurred in Changer: {e}")
            time.sleep(1)  # Retry after delay



class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

@bot.command()
async def gc1(ctx, gc_id: int):
    if gc_id in running_threads:
        await ctx.send(f"Actions are already running in GC {gc_id}. Use !gc_end {gc_id} to stop them first.")
        return

    changer_thread = StoppableThread(target=Changers, args=(gc_id,))


    running_threads[gc_id] = [changer_thread]
    

    changer_thread.start()
   

    await ctx.send(f"Starting actions in GC {gc_id}.")
    

@bot.command()
async def gcend(ctx, gc_id: int):
    if gc_id not in running_threads:
        await ctx.send(f"No actions running in GC {gc_id}.")
        return

    threads = running_threads.pop(gc_id)
    for thread in threads:
        thread.stop()
        thread.join()

    

    await ctx.send(f"discord.gg/chatpacking")

running_threads = {}

class StoppableThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def spam_messages(channel_id):
    global spam_counter  # Declare spam_counter as a global variable
    while not threading.current_thread().stopped():
        try:
            random_message = random.choice(Regular_Spammer_Message)

            response = requests.post(
                f"https://discordapp.com/api/v6/channels/{channel_id}/messages",
                headers={"Authorization": TOKEN},
                json={"content": f"{random_message} {spam_counter}"}
            )
            response.raise_for_status()
            spam_counter += 1  # Increment spam_counter
            time.sleep(1)  # Adjust the delay between messages as needed
        except Exception as e:
            print(f"An error occurred in spam_messages: {e}")
            time.sleep(1)  # Retry after delay

@bot.command()
async def gc2(ctx, gc_id: int):
    if gc_id in running_threads:
        await ctx.send(f"Actions are already running in GC {gc_id}. Use !gc_end {gc_id} to stop them first.")
        return

    
    spam_thread = StoppableThread(target=spam_messages, args=(gc_id,))
    

    running_threads[gc_id] = [ spam_thread]
   

   
    spam_thread.start()

    await ctx.send(f"Starting actions in GC {gc_id}.")
   

@bot.command()
async def gcend2(ctx, gc_id: int):
    if gc_id not in running_threads:
        await ctx.send(f"No actions running in GC {gc_id}.")
        return

    threads = running_threads.pop(gc_id)
    for thread in threads:
        thread.stop()
        thread.join()

 
    await ctx.send(f"discord.gg/chatpacking")

@bot.command()
async def feed(ctx, user: discord.Member=None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/feed")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention, file=discord.File(file, f"astraa_feed.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)

@bot.command()
async def tickle(ctx, user: discord.Member=None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    r = requests.get("https://nekos.life/api/v2/img/tickle")
    res = r.json()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention, file=discord.File(file, f"astraa_tickle.gif"))
    except:
        em = discord.Embed(description=user.mention)
        em.set_image(url=res['url'])
        await ctx.send(embed=em)


# Run the bot
bot.run(TOKEN, bot=False)