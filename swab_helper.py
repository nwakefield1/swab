import discord
import re
import pafy
import os

from callbacks import PafyCallback

class SWABHelper:
    def __init__(self, client):
        self.client = client

    def is_me(self, message):
        return message.author == self.client.user

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
