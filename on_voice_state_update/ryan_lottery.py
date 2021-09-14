import random

from settings import music


async def ryan_lottery(member, before, after):
    if before.channel is None and after.channel is not None:
        lottery = random.randrange(100)
        if lottery == 69:  # ryan should get a 1/100 chance for poophead to play
            await music.play(
                channel=after.channel,
                message=None,
                url='https://www.youtube.com/watch?v=trj0Jy6Kfo8',
                to_front=True,
                stop_current=True
            )
