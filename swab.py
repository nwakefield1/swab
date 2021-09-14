import os
import random
from dotenv import load_dotenv

from settings import client, interesting_ids, swab, music

from bot_functions import (
    clean,
    make_swan_go_back_to_work,
    play,
    poophead,
    skip,
    pause,
    resume,
    clear_queue
)


@client.event
async def on_message(message):
    if message.content.startswith('~werk'):
        await make_swan_go_back_to_work(message)

    if message.content.startswith('~clean'):
        await clean(message)

    if message.content.startswith('~poophead'):
        await poophead(message)

    if message.content.startswith('~play'):
        await play(message)

    if message.content.startswith('~skip'):
        await skip(message)

    if message.content.startswith('~pause'):
        await pause(message)

    if message.content.startswith('~resume') or message.content.startswith('~continue'):
        await resume(message)

    if message.content.startswith('~clear') or message.content.startswith('~clearqueue'):
        await clear_queue(message)


@client.event
async def on_voice_state_update(member, before, after):
    if member.id == interesting_ids['ryan']:
        if before.channel is None and after.channel is not None:
            lottery = random.randrange(100)
            if lottery == 69:  # ryan should get a 1/100 chance for poophead to play
                channel = after.channel
                voice_client = await swab.get_voice_client(channel, client)

                if channel != voice_client.channel:
                    await voice_client.disconnect()
                    voice_client = await swab.get_voice_client(channel, client)

                path = await music.get_file_path_from_url(None, voice_client, 'https://www.youtube.com/watch?v=trj0Jy6Kfo8')
                if path is not None:
                    # if path is None, a video is being downloaded and PafyCallback will handle this
                    music.add_to_queue(path, to_front=True)
                    voice_client.stop()
                if not voice_client.is_playing():
                    # if not playing, play the song in the queue
                    music.play_song(voice_client)

load_dotenv()
client.run(os.getenv("SWAB_TOKEN"))
