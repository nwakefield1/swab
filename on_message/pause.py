from settings import client


async def pause(message):
    client.voice_clients[0].pause()
