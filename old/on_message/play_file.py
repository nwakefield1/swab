import aiohttp

import os
from urllib.parse import urlparse

from settings import music


async def get_path(message):
    attachment_url = message.attachments[0].proxy_url
    parsed_url = urlparse(attachment_url)
    file_name = os.path.basename(parsed_url.path)
    async with aiohttp.ClientSession() as session:
        url = message.attachments[0].proxy_url
        async with session.get(url) as resp:
            if resp.status == 200:
                file_data = await resp.read()
                path = f"custom_audio/{file_name}"
                file = open(path, mode='wb')
                file.write(file_data)
                file.close()
    return attachment_url, file_name, path


async def play_file(
        message=None, channel=None, attachment_url=None, file_name=None, path=None, to_front=False, stop_current=False):

    if path is None:
        attachment_url, file_name, path = get_path(message)

    if message is not None:
        channel = message.author.voice.channel
    elif channel is not None:
        channel = channel
    else:
        raise Exception("Requires at least message or channel")

    voice_client = await music.swab_helper.get_voice_client(channel, music.client)
    if channel != voice_client.channel:  # disconnect the bot to follow the user
        await voice_client.disconnect()
        voice_client = await music.swab_helper.get_voice_client(channel, music.client)
    if path is not None:
        # if path is None, a video is being downloaded and PafyCallback will handle this
        music.add_to_queue(path, to_front)
        music.playlist_data.append({
            'title': file_name,
            'length': 0,
            'url': attachment_url
        })
    if not voice_client.is_playing():
        # if not playing, play the song in the queue
        await music.play_song_wrapper(voice_client, voice_client.channel)
