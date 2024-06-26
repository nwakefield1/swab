import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.environ.get('SWAB_TOKEN', '')
LRL_ID = '234021611236360193'

interesting_ids = {
    'nathan': 234020073281421312,
    'loc': 253709501830529026,
    'ryan': 257014900486832128,
    'swan': 193631636032585728,
    'colten': 296510813219323904,
    'pete': 266240571901870082,
    'john': 187058095250341888
}

command_list = []

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True
client = discord.Client(intents=intents)

swab_bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("~"),
    description='SWAB 2.0 Bot',
    intents=intents,
)

# channel shorcuts // does not work
# general_channel = client.get_channel(234021611236360193)
# music_bot_channel = client.get_channel(620760286781112358)
