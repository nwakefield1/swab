from settings import client


async def pause(message):
    voice_clients = client.voice_clients
    if len(voice_clients) > 0 and voice_clients[0].is_playing():
        voice_clients[0].pause()
        await message.channel.send('Paused <:WICKED:827289802339516428>')
    else:
        await message.channel.send('Nothing playing, can\'t pause <:tommy:880566693355745300>')
