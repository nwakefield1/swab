import discord

from on_message.play_file import play_file
from settings import music


async def play(message: discord.Message):
    has_attachment = len(message.attachments) > 0
    if has_attachment:
        await play_file(message)
    else:
        await music.play(
            channel=message.author.voice.channel,
            message=message,
            url=None,
            to_front=False,
            stop_current=False,
            resume_song=True
        )
