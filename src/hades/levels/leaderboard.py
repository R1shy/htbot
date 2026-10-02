import os
import logging
import aiohttp
from discord import Embed, Interaction
from discord import Webhook

async def leaderboard(interaction: Interaction):
    logger = logging.getLogger("discord")
    url: str = os.getenv("LEADERBOARD_WEBHOOK_URL") or "NoURL"
    if url == "NoURL":
        logger.error("LEADERBOARD URL NOT DEFINED")
        await interaction.response.send_message("Internal Error")
    else:
        async with aiohttp.ClientSession() as session:
            wh = Webhook.from_url(url=url,session=session)
            whc = wh.source_channel
            if whc is None:
                await interaction.response.send_message("Not in a channel!")
            else:
                if interaction.channel_id != whc.id:
                    await interaction.response.send_message(f"Wrong channel please send in {whc.mention}")
                else:
                    emb = Embed(title="Meow")
                    await wh.send(embed=emb)
