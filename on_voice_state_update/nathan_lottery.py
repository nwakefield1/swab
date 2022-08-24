import random

from settings import music


async def nathan_lottery(member, before, after):
    # member first enters chat
    if before.channel is None and after.channel is not None:
        print('Attempting to lottery Nathan')
        lottery = random.randrange(100)
        if lottery == 69:  # nathan should get a 1/100 chance for cbt to play
            print(f'{lottery}: Nathan is a CBT :dddd')
            await music.play(
                channel=after.channel,
                message=None,
                url='https://www.youtube.com/watch?v=0bkqm4LbZgI',
                to_front=True,
                stop_current=True
            )
        else:
            print(f'{lottery}: Failed. Nathan is not a CBT ;)')
