from settings import client, music


async def clear_queue(message):
    # Annoyingly prepends SKULL TRUMPET to the front of the music queue whenever someone skips a song
    music.clear_queue()
    path = await music.get_file_path_from_url(
        message=None,
        voice_client=client.voice_clients[0],
        url='https://www.youtube.com/watch?v=eVrYbKBrI7o',
        to_front=True
    )
    if path is not None:
        music.add_to_queue(path, to_front=True)
    client.voice_clients[0].stop()
