from settings import music


async def cbt_island_boys(message):
    await message.channel.send('<a:_:1011787126968426516>')
    try:
        await music.play(
            channel=message.author.voice.channel,
            message=None,
            url='https://www.youtube.com/watch?v=0bkqm4LbZgI',
            to_front=False,
            stop_current=False
        )
    except Exception as e:
        print(e)
        await message.channel.send('Must be in voice channel for CBT')
