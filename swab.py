import os

from dotenv import load_dotenv

from settings import client, interesting_ids

from on_message import (
    clean,
    make_swan_go_back_to_work,
    play,
    play_file,
    poophead,
    skip,
    pause,
    resume,
    clear_queue,
    view_queue
)

from on_voice_state_update import (
    leave_channel,
    ryan_lottery
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

    if message.content.startswith('~fplay'):
        await play_file(message)

    if message.content.startswith('~skip'):
        await skip(message)

    if message.content.startswith('~pause'):
        await pause(message)

    if message.content.startswith('~resume') or message.content.startswith('~continue'):
        await resume(message)

    if message.content.startswith('~clear') or message.content.startswith('~clearqueue'):
        await clear_queue(message)

    if message.content.startswith('~queue') or message.content.startswith('~viewqueue'):
        await view_queue(message)


@client.event
async def on_voice_state_update(member, before, after):
    if member.id == client.user.id:  # if is bot
        await leave_channel(member, before, after)

    if member.id == interesting_ids['ryan']:
        await ryan_lottery(member, before, after)

load_dotenv()
client.run(os.getenv("SWAB_TOKEN"))
