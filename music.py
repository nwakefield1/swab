import os
import asyncio
import discord
import json
import pafy

from youtube_search import YoutubeSearch

from callbacks import PafyCallback


class Music:
    def __init__(self, client, swab_helper):
        self.client = client
        self.swab_helper = swab_helper
        self.playlist = []
        self.current_song_playing = None

    def play_song(self, voice_client):
        source = discord.FFmpegOpusAudio(self.playlist[0], options={'use_wallclock_as_timestamps': True})
        voice_client.play(source, after=self.play_after)
        self.playlist.pop(0)
        self.current_song_playing = source

    def play_after(self, error):
        try:
            future = asyncio.run_coroutine_threadsafe(self.play_song(self.client.voice_clients[0]), None)
            future.result()
        except IndexError:
            pass

    def add_to_queue(self, file_path):
        """
        adds a song to the playlist queue
        """
        self.playlist.append(file_path)

    async def get_file_path_from_url(self, message, voice_client):
        url = message.content.split('~play')[1]
        if not self.swab_helper.validate_url(url):
            response = json.loads(YoutubeSearch(url, max_results=1).to_json())['videos'][0]
            title = response['title']
            duration = response['duration']
            url_suffix = response['url_suffix']
            url = 'https://www.youtube.com{}'.format(url_suffix)
            await message.channel.send(f'Found video: {title} ({duration})\n{url}')
        else:
            url = url.strip()
        video = pafy.new(url)
        best = video.getbestaudio()
        file_path = 'music/{}.{}'.format(video.videoid, best.extension)
        if os.path.exists(file_path):
            return file_path
        else:
            best.download(filepath=file_path, callback=PafyCallback(self, file_path, voice_client))
        return None

