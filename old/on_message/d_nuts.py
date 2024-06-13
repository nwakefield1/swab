import random


async def d_nuts(message):
    lottery_number = random.randint(0, 100)
    print(lottery_number)
    if lottery_number == 69:
        await message.channel.send(f'{message.content} deez nuts')
