import os

from discord import Interaction
from discord.channel import ForumChannel


async def audcount(interaction: Interaction):
    audchannelid = os.getenv("AUDCHANNELID") or "-1"
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("Not in a server")
    else:
        channel = await guild.fetch_channel(int(audchannelid))
        if isinstance(channel, ForumChannel):
            threads = channel.threads
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(
                        f"{len(threads)} auditions so far!"
                    )
            except Exception as e:
                print(f"err2: {e!s}")
