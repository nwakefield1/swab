from settings import client, swab, music


async def poophead(message):
    try:
        channel = message.author.voice.channel
        voice_client = await swab.get_voice_client(channel, client)
        path = await music.get_file_path_from_url(None, voice_client, 'https://www.youtube.com/watch?v=trj0Jy6Kfo8')
        if path is not None:
            # if path is None, a video is being downloaded and PafyCallback will handle this
            music.add_to_queue(path)
        if not voice_client.is_playing():
            # if not playing, play the song in the queue
            music.play_song(voice_client)
    except Exception as e:
        print(e)
        await message.channel.send('Must be in voice channel for poophead')
