import discord
import os
import time
import random
import json

from discord.ext import commands
from dotenv import load_dotenv
from youtube_search import YoutubeSearch

from music import Music
from swab_helper import SWABHelper

interesting_ids = {
    'nathan': '234020073281421312',
    'loc': '253709501830529026',
    'ryan': '257014900486832128',
    'swan': '193631636032585728',
    'colten': '296510813219323904',
    'pete': '266240571901870082',
    'john': '187058095250341888'
}

command_list = [
    '~werk',
    '~clean',
    '~play',
    '~poophead'
]


client = discord.Client()
bot = commands.Bot(command_prefix='~')
s = SWABHelper(client=client)
music = Music(client=client, swab_helper=s)

@client.event
async def on_message(message):
    if message.content.startswith('~werk'):
        users = client.users
        commands = message.content.split('~werk')
        if len(commands) > 1:
            times = int(commands[1].strip())
        else:
            times = 1

        for user in users:
            if str(user.id) == interesting_ids['swan']:
                swan = user
                for i in range(0, times):                
                    await message.channel.send(swan.mention + ' go back to work')
                    time.sleep(random.randint(0, 60))

    if message.content.startswith('~clean'):
        deleted = await message.channel.purge(limit=100, check=s.is_me_or_command)
        await message.channel.send('Deleted {} message(s)'.format(len(deleted)))
        await message.channel.purge(limit=100, check=s.is_me_or_command)

    if message.content.startswith('~poophead'):
        channel = message.author.voice.channel
        vc = await s.get_voice_client(channel, client)
        url = 'https://www.youtube.com/watch?v=trj0Jy6Kfo8'
        await s.get_audio_url(url, vc)

    if message.content.startswith('~play'):
        channel = message.author.voice.channel
        voice_client = await s.get_voice_client(channel, client)

        if channel != voice_client.channel:
            await voice_client.disconnect()
            voice_client = await s.get_voice_client(channel, client)

        path = music.get_file_path_from_url(message, voice_client)
        if path is not None:
            # if path is None, a video is being downloaded and PafyCallback will handle this
            music.add_to_queue(path)        
        if not voice_client.is_playing():
            # if not playing, play the song in the queue
            music.play_song(voice_client)


@client.event
async def on_voice_state_update(member, before, after):
    if str(member.id) == interesting_ids['ryan']:
        if before.channel is None and after.channel is not None:
            vc = await s.get_voice_client(after.channel, client)
            url = 'https://www.youtube.com/watch?v=trj0Jy6Kfo8'
            await s.get_audio_url(url, vc)

load_dotenv()
client.run(os.getenv("SWAB_TOKEN"))