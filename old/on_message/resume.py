from settings import client


async def resume(message):
    voice_clients = client.voice_clients
    if len(voice_clients) > 0 and voice_clients[0].is_paused():
        voice_clients[0].resume()
        await message.channel.send('Unpaused go back to work <:hahaa:631585125607538688>')
    else:
        await message.channel.send('Nothing paused you SUSSY BAKA, can\'t resume <:buccer:847875411773751327>')
