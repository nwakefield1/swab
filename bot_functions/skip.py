from settings import client


async def skip(message):
    client.voice_clients[0].stop()
