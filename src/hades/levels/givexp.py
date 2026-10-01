import logging
import os
from logging import Logger

from discord import Interaction, Member

from hades.globals import gcursor


async def ge(interaction: Interaction, addamount: int, user: Member):
    logger: Logger = logging.getLogger("discord")
    await interaction.response.defer(ephemeral=True)
    adminid: int = int(os.getenv("ADMINROLEID") or "-1")
    modid: int = int(os.getenv("MODROLEID") or "-1")
    if adminid == -1:
        logger.error("ADMINROLEID not set!")
        await interaction.followup.send("Internal error, try again later")
    elif modid == -1:
        logger.error("MODROLEID not set!")
        await interaction.followup.send("Internal error, try again later")
    else:
        if isinstance(interaction.user, Member):
            u: Member = interaction.user
            roles = [r.id for r in u.roles]
            if modid not in roles and adminid not in roles:
                print(u.roles)
                await interaction.followup.send("You don't have perms for this!")
            else:
                gcursor.execute(
                    """
                                UPDATE levels SET exp = exp + ? WHERE uid = ?;
                                """,
                    [addamount, user.id],
                )
                gcursor.execute(
                    """
                                SELECT EXP FROM levels WHERE uid = ?;
                                """,
                    [user.id],
                )
                await interaction.followup.send(f"New exp is {gcursor.fetchone()[0]}")
