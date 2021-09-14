from settings import music


async def poophead(message):
    try:
        await music.play(
            channel=message.author.voice.channel,
            message=None,
            url='https://www.youtube.com/watch?v=trj0Jy6Kfo8',
            to_front=False,
            stop_current=False
        )
    except Exception as e:
        print(e)
        await message.channel.send('Must be in voice channel for poophead')
