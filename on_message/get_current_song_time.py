import datetime

from settings import music


async def get_current_song_time(message):
    if len(music.client.voice_clients) > 0 and music.client.voice_clients[0].is_playing():
        current_song_at = music.get_song_at()
        current_song_length = music.current_song_playing['length']
        current_song_title = music.current_song_playing["title"]
        current_song_at_seconds = datetime.datetime.strptime(current_song_at, '%H:%M:%S')
        current_song_at_seconds = datetime.timedelta(
            hours=current_song_at_seconds.hour,
            minutes=current_song_at_seconds.minute,
            seconds=current_song_at_seconds.second
        )
        current_song_length_seconds = datetime.datetime.strptime(current_song_length, '%H:%M:%S')
        current_song_length_seconds = datetime.timedelta(
            hours=current_song_length_seconds.hour,
            minutes=current_song_length_seconds.minute,
            seconds=current_song_length_seconds.second
        )
        difference = round(current_song_at_seconds.total_seconds()/current_song_length_seconds.total_seconds(), 1)
        playbar = '────────────────────'
        _playbar = list(playbar)
        _playbar[int(difference*10*2)] = '⚪'
        playbar = "".join(_playbar)

        await message.channel.send(
            f'ɴᴏᴡ ᴘʟᴀʏɪɴɢ: \n{current_song_title} '
            f'{playbar} ◄◄⠀▶⠀►►⠀ '
            f'{current_song_at} / {current_song_length} ⠀ '
            f'───○ 🔊 ᴴᴰ ⚙️'
        )
    else:
        await message.channel.send(':shrug:')
