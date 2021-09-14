from settings import client, music


async def clear_queue(message):
    # Annoyingly prepends SKULL TRUMPET to the front of the music queue whenever someone skips a song
    music.clear_queue()
    path = await music.get_file_path_from_url(None, client.voice_clients[0], 'https://www.youtube.com/watch?v=eVrYbKBrI7o')
    if path is not None:
        music.add_to_queue(path, to_front=True)
    client.voice_clients[0].stop()
