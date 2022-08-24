import os

from dotenv import load_dotenv

from settings import client, interesting_ids

from on_message import (
    clean,
    make_swan_go_back_to_work,
    play,
    play_file,
    poophead,
    cbt_island_boys,
    skip,
    pause,
    resume,
    clear_queue,
    view_queue,
    get_current_song_time
)

from on_voice_state_update import (
    leave_channel,
    lottery,
    ryan_lottery,
    nathan_lottery
)


@client.event
async def on_message(message):
    # make commands case insensitive, because of this, I may not be able to use discord.Command.
    # i hate my friends

    message_content = message.content.lower()

    if message_content.startswith('~werk'):
        await make_swan_go_back_to_work(message)

    if message_content.startswith('~clean'):
        await clean(message)

    if message_content.startswith('~poophead'):
        await poophead(message)

    if message_content.startswith('~cbt'):
        await cbt_island_boys(message)

    if message_content.startswith('~play'):
        await play(message)

    if message_content.startswith('~fplay'):
        await play_file(message)

    if message_content.startswith('~skip') or message_content.startswith('~next'):
        await skip(message)

    if message_content.startswith('~pause') or message.content.startswith('~stop'):
        await pause(message)

    if (
            message_content.startswith('~resume')
            or message.content.startswith('~continue')
            or message.content.startswith('~start')
    ):
        await resume(message)

    if message_content.startswith('~clear') or message.content.startswith('~clearqueue'):
        await clear_queue(message)

    if message_content.startswith('~queue') or message.content.startswith('~viewqueue'):
        await view_queue(message)

    if message_content.startswith('~span') or message.content.startswith('~current'):
        await get_current_song_time(message)


@client.event
async def on_voice_state_update(member, before, after):
    if member.id == client.user.id:  # if is bot
        await leave_channel(member, before, after)

    # play poophead 1/100 chance whenever ryan joins a channel
    if member.id == interesting_ids['ryan']:
        await lottery(member, before, after, 'ryan')

    # play island boys 1/100 chance whenever nathan joins a channel
    if member.id == interesting_ids['nathan']:
        await lottery(member, before, after, 'nathan')

load_dotenv()
client.run(os.getenv("SWAB_TOKEN"))
