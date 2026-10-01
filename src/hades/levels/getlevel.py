import logging

from discord import Interaction

from hades.globals import gcursor


async def gl(interaction: Interaction):
    logger = logging.getLogger("discord")
    await interaction.response.defer(ephemeral=True)
    user = interaction.user
    uid = user.id
    try:
        gcursor.execute("SELECT exp FROM levels WHERE uid = ?", [uid])
        r = gcursor.fetchone()
        if r is None:
            await interaction.followup.send(
                "You have sent no messages, send a message to get a level"
            )
        else:
            if isinstance(r[0], int):
                await interaction.followup.send(
                    f"your level is {int(r[0] / 100)}, raw exp: {r[0]}"
                )
    except Exception as e:
        logger.error(str(e))
        await interaction.followup.send("it break")
