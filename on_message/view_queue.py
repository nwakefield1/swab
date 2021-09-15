from settings import music


async def view_queue(message):
    playlist_data = music.get_playlist_data()

    if not playlist_data:
        await message.channel.send('Nothing in queue')
        return

    playlist_text = ''
    for index, song in enumerate(playlist_data):
        if index == 0:
            playlist_text += f"**Now Playing: {song['title']} - {song['length']} (<{song['url']}>)**\n"
        elif index == 1:
            playlist_text += f"Next: {song['title']} - {song['length']} (<{song['url']}>)\n"
        else:
            playlist_text += f"{song['title']} - {song['length']} (<{song['url']}>)\n"

    await message.channel.send(playlist_text)
