from settings import swab


async def clean(message):
    deleted = await message.channel.purge(limit=100, check=swab.is_me_or_command)
    await message.channel.send(f'Deleted {len(deleted)} message(s)')
    await message.channel.purge(limit=100, check=swab.is_me_or_command)
