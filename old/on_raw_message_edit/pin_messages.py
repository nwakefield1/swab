import discord


async def already_embedded(channel, message_id):
    all_messages = await channel.history(limit=100).flatten()
    for message in all_messages:
        if message.embeds:
            embed_footer_text = message.embeds[0].footer.text
            try:
                if str(message_id) in embed_footer_text:
                    return True
            except TypeError as e:
                print(e)
                pass
    return False


async def pin_messages(client, channel_id, message_id):
    origin_channel = await client.fetch_channel(channel_id)
    origin_message = await origin_channel.fetch_message(message_id)
    pin_channel_id = 1088601843602554980 if origin_channel.nsfw else 1088599521103204352
    pin_channel = await client.fetch_channel(pin_channel_id)

    # we don't want to pin messages multiple times
    message_embedded = await already_embedded(origin_channel, message_id)
    if message_embedded:
        return

    # todo: i think this is being returned as a string, not datetime.datetime, check and convert it later
    # message_created = origin_message.created_at.astimezone(pytz.timezone('US/Pacific')).strftime("%m-%d-%Y %I:%M:%S %p")
    quote_embed = discord.Embed(
        description=f'[[Source]]({origin_message.jump_url})\n{origin_message.content}'
    )
    quote_embed.set_author(
        name=origin_message.author.display_name,
        icon_url=origin_message.author.avatar_url
    )
    quote_embed.set_footer(
        text=f'{origin_message.id}',
    )
    if origin_message.attachments:
        quote_embed.set_image(url=origin_message.attachments[0].url)
    elif origin_message.embeds:
        if origin_message.embeds[0].thumbnail:
            quote_embed.set_image(url=origin_message.embeds[0].thumbnail.url)
        else:
            quote_embed.set_image(url=origin_message.embeds[0].image.url)

    await pin_channel.send(embed=quote_embed)
