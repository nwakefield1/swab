import random
import time

from settings import client, interesting_ids


async def make_swan_go_back_to_work(message):
    commands = message.content.split('~werk')
    try:
        times = int(commands[1].strip())
    except ValueError:
        times = 1

    swan = client.get_user(id=interesting_ids['swan'])

    for i in range(0, times):
        await message.channel.send(swan.mention + ' go back to work')
        if i + 1 < times:
            time.sleep(random.randint(0, 60))
