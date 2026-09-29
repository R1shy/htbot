

import logging

from hades.globals import gcursor
from discord import Interaction


async def gl(interaction: Interaction):
    logger = logging.getLogger("discord")
    await interaction.response.defer(ephemeral=True)
    user = interaction.user
    uid = user.id
    try:
        gcursor.execute("SELECT exp FROM levels WHERE uid = ?", [uid])
        e = gcursor.fetchone()[0]
        if isinstance(e, int):
            await interaction.followup.send(f"your level is {int(e/100)}")
    except Exception as e:
        logger.error(str(e))
        await interaction.followup.send("it break")
