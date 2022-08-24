import random

from settings import music


def get_lottery_settings(member_name):
    if member_name == 'nathan':
        lottery_settings = {
            'success_text': '{}: Nathan is a CBT :dddd',
            'fail_text': '{}: Nathan is not a CBT ;)',
            'url': 'https://www.youtube.com/watch?v=0bkqm4LbZgI'
        }
    elif member_name == 'ryan':
        lottery_settings = {
            'success_text': '{}: Ryan is a poophead.',
            'fail_text': '{}: Ryan is not a poophead.',
            'url': 'https://www.youtube.com/watch?v=trj0Jy6Kfo8'
        }
    return lottery_settings


async def lottery(member, before, after, member_name):
    lottery_settings = get_lottery_settings(member_name)
    music_bot_channel = music.client.get_channel(620760286781112358)
    # member first enters chat
    if before.channel is None and after.channel is not None:
        lottery = random.randrange(100)
        if lottery == 69:  # nathan should get a 1/100 chance for cbt to play
            await music_bot_channel.send(lottery_settings['success_text'].format(lottery))
            await music.play(
                channel=after.channel,
                message=None,
                url=lottery_settings['url'],
                to_front=True,
                stop_current=True
            )
        else:
            await music_bot_channel.send(lottery_settings['fail_text'].format(lottery))
