import discord
import pafy
import re
import json
import tempfile
import os

from dotenv import load_dotenv
from youtube_search import YoutubeSearch

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


class SWABHelper:
    def __init__(self):
        pass

    @staticmethod
    def is_me(message):
        return message.author == client.user

    @staticmethod
    def is_command(message):
        return message.content.startswith('~')

    @staticmethod
    def validate_url(url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(regex, url)

    @staticmethod
    async def get_voice_client(channel, _client):
        try:
            vc = await channel.connect()
        except discord.errors.ClientException:
            vc = _client.voice_clients[0]
        return vc

    async def get_audio_url(self, url, vc):
        video = pafy.new(url)
        best = video.getbestaudio()   
        file_path = 'music/{}.{}'.format(video.videoid, best.extension)
        if os.path.exists(file_path):
            await SWABHelper().play_audio(file_path, vc)
        else:
            audio = best.download(filepath=file_path, callback=PafyCallback(file_path, vc))

    async def play_audio(self, file_path, vc):
        options = {
            'probesize': '24M'
        }
        source = await discord.FFmpegOpusAudio.from_probe(file_path, options=options)
        vc.play(source)

    def is_me_or_command(self, message):
        return self.is_me(message) or self.is_command(message)

class PafyCallback():
    def __init__(self, file_path, vc):
        self.vc = vc
        self.file_path = file_path

    def __call__(self, total, recvd, ratio, rate, eta):
        if ratio == 1.0:        
            audio = discord.FFmpegOpusAudio(self.file_path)
            self.vc.play(audio)

s = SWABHelper()
client = discord.Client()


@client.event
async def on_message(message):
    if message.content.startswith('~werk'):
        users = client.users
        for user in users:
            if str(user.id) == '193631636032585728':
                swan = user
                await message.channel.send(swan.mention + ' go back to work')

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
        url = message.content.split('~play')[1]
        if not s.validate_url(url):
            results = json.loads(YoutubeSearch(url, max_results=1).to_json())['videos'][0]['link']
            url = 'https://www.youtube.com/{}'.format(results)
        else:
            url = url.strip()
        vc = await s.get_voice_client(channel, client)
        await s.get_audio_url(url, vc)


@client.event
async def on_voice_state_update(member, before, after):
    if str(member.id) == '257014900486832128':
        if before.channel is None and after.channel is not None:
            vc = await s.get_voice_client(after.channel, client)
            url = 'https://www.youtube.com/watch?v=trj0Jy6Kfo8'
            await s.get_audio_url(url, vc)

load_dotenv()
client.run(os.getenv("SWAB_TOKEN"))