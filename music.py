import os
import asyncio
import datetime
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
        self.playlist_data = []

    def play_song(self, voice_client: discord.VoiceClient) -> None:
        """
        Plays the first song in the playlist queue.

        :param voice_client: The discord VoiceClient that the bot should play into.
        :return: None
        """
        source = discord.FFmpegOpusAudio(self.playlist[0], options={'use_wallclock_as_timestamps': True})
        voice_client.play(source, after=self.play_after)
        self.playlist.pop(0)
        self.current_song_playing = self.playlist_data.pop(0)

    def play_after(self, error) -> None:
        """
        Used as a callback to play a song after the current one is done playing.

        :param error: Not used.
        :return: None
        """
        try:
            future = asyncio.run_coroutine_threadsafe(self.play_song(self.client.voice_clients[0]), None)
            future.result()
        except TypeError as e:
            if 'A coroutine object is required' in e:
                pass
            raise e
        except IndexError:
            pass

    def get_playlist_data(self) -> list[object]:
        """
        Get data on all the songs in the playlist.

        :return: A list of objects that describes each song in the playlist. Or an empty list.
        """
        if not self.client.voice_clients:
            # If not connected to any voice clients, return empty list
            return []
        if self.client.voice_clients and not self.client.voice_clients[0].is_playing():
            # If connected to a voice client and not playing, return empty list
            return []
        return [self.current_song_playing] + self.playlist_data

    def clear_queue(self) -> None:
        """
        Clears the music queue

        :return: None
        """
        self.playlist = []
        self.playlist_data = []
        self.current_song_playing = None

    def add_to_queue(self, file_path: str, to_front: bool = False) -> None:
        """
        Adds a song to the playlist queue.

        :param file_path: File path that describes where the audio file is located.
        :param to_front: Should the song be added to the front or back of the queue?
        :return:
        """
        if to_front:
            self.playlist.insert(0, file_path)
        else:
            self.playlist.append(file_path)

    async def get_youtube_url(self, search_param: str, message: discord.Message) -> str:
        """
        Returns a YouTube url given search params and a discord Message object.

        :param search_param: The search parameters to use on YouTube
        :param message: A discord message object to respond to
        :return: A YouTube url to download songs from
        """
        response = json.loads(YoutubeSearch(search_param, max_results=1).to_json())['videos'][0]
        title = response['title']
        duration = response['duration']
        url_suffix = response['url_suffix']
        url = 'https://www.youtube.com{}'.format(url_suffix)
        await message.channel.send(f'Found video: {title} ({duration})\n{url}')
        return url

    async def get_file_path_from_url(
            self,
            message: discord.Message,
            voice_client: discord.VoiceClient,
            url: str = None,
            to_front: bool = False
    ) -> str:
        """
        Handles all the logic of getting an audio file from YouTube, as well as keeping track of the song data in
        playlist_data.

        :param message: The discord Message object that contains either a YouTube link or search string.
        :param voice_client: The discord VoiceClient that the bot should play into.
        :param url: Optional, can directly input a url to use instead of using a discord Message.
        :param to_front: Should the music data be added to the front of playlist_data? (Used for skeleton doot)
        :return: A file path to the related audio file.
        """
        if not url:
            url = message.content.split('~play')[1]

        # If the user did not input a YouTube url, search YouTube for a related video
        if not self.swab_helper.validate_url(url):
            url = await self.get_youtube_url(url, message)
        else:
            url = url.strip()

        video = pafy.new(url)
        video_data = {
            'title': video.title,
            'length': str(datetime.timedelta(seconds=video.length)),
            'url': url
        }

        if to_front:
            self.playlist_data.insert(0, video_data)
        else:
            self.playlist_data.append(video_data)

        best = video.getbestaudio()
        file_path = 'music/{}.{}'.format(video.videoid, best.extension)
        if os.path.exists(file_path):
            return file_path
        else:
            best.download(filepath=file_path, callback=PafyCallback(self, file_path, voice_client))
        return None

    async def play(
            self,
            channel: discord.TextChannel,
            message: discord.Message,
            url: str,
            to_front: bool = False,
            stop_current: bool = False,
            resume_song: bool = False
    ) -> None:
        """
        Will play a song or resume a song if one is currently paused.

        :param channel: The discord TextChannel to respond to.
        :param message: The discord Message that describes the origin of the command.
        :param url: The url that describe the YouTube video to be played.
        :param to_front: Should the song be added to the front or back of the queue?
        :param stop_current: Should the current song be hijacked to play the incoming song request?
        :param resume_song: Should the some be resumed if the bot is paused?
        :return:
        """
        voice_client = await self.swab_helper.get_voice_client(channel, self.client)
        if resume_song and voice_client.is_paused():
            # Exit condition to resume song if player is currently paused
            from on_message import resume
            await resume(message)
            return

        path = await self.get_file_path_from_url(message, voice_client, url)

        if channel != voice_client.channel:
            await voice_client.disconnect()
            voice_client = await self.swab_helper.get_voice_client(channel, self.client)

        if path is not None:
            # if path is None, a video is being downloaded and PafyCallback will handle this
            self.add_to_queue(path, to_front)
            if stop_current:
                voice_client.stop()
        if not voice_client.is_playing():
            # if not playing, play the song in the queue
            self.play_song(voice_client)
