import os
from dotenv import load_dotenv

from settings import client
from bot_functions import (
    clean,
    make_swan_go_back_to_work,
    play,
    poophead,
    skip
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

    if message.content.startswwith('~pause'):
        await pause(message)

    if message.content.startswith('~resume') or message.content.startswith('~continue'):
        await resume(message)

# @client.event
# async def on_voice_state_update(member, before, after):
#     if str(member.id) == interesting_ids['ryan']:
#         if before.channel is None and after.channel is not None:
#             vc = await s.get_voice_client(after.channel, client)
#             url = 'https://www.youtube.com/watch?v=trj0Jy6Kfo8'
#             await s.get_audio_url(url, vc)

load_dotenv()
client.run(os.getenv("SWAB_TOKEN"))
