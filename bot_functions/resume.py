from settings import client


async def resume(message):
    client.voice_clients[0].resume()
