from settings import music


async def play(message):
    await music.play(
        channel=message.author.voice.channel,
        message=message,
        url=None,
        to_front=False,
        stop_current=False,
        resume_song=True
    )
