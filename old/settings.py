import discord
from discord.ext import commands

from music import Music
from swab_helper import SWABHelper

interesting_ids = {
    'nathan': 234020073281421312,
    'loc': 253709501830529026,
    'ryan': 257014900486832128,
    'swan': 193631636032585728,
    'colten': 296510813219323904,
    'pete': 266240571901870082,
    'john': 187058095250341888
}

command_list = [
    '~werk',
    '~clean',
    '~play',
    '~poophead',
    '~skip',
    '~pause',
    '~resume/~continue',
    '~clear/~clearqueue'
]

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='~')
swab = SWABHelper(client=client)
music = Music(client=client, swab_helper=swab)

# channel shorcuts // does not work
# general_channel = client.get_channel(234021611236360193)
# music_bot_channel = client.get_channel(620760286781112358)
