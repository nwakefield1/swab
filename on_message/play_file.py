import aiohttp

import os
from urllib.parse import urlparse

from settings import music


async def play_file(message):
    path = None
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

    voice_client = await music.swab_helper.get_voice_client(message.author.voice.channel, music.client)
    if path is not None:
        # if path is None, a video is being downloaded and PafyCallback will handle this
        music.add_to_queue(path, False)
        music.playlist_data.append({
            'title': file_name,
            'length': 0,
            'url': attachment_url
        })
    if not voice_client.is_playing():
        # if not playing, play the song in the queue
        await music.play_song_wrapper(voice_client)
