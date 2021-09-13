from settings import client, music, swab


async def play(message):
    channel = message.author.voice.channel
    voice_client = await swab.get_voice_client(channel, client)

    if channel != voice_client.channel:
        await voice_client.disconnect()
        voice_client = await swab.get_voice_client(channel, client)

    path = await music.get_file_path_from_url(message, voice_client)
    if path is not None:
        # if path is None, a video is being downloaded and PafyCallback will handle this
        music.add_to_queue(path)
    if not voice_client.is_playing():
        # if not playing, play the song in the queue
        music.play_song(voice_client)
