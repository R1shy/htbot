import logging
from logging import Logger

from discord import Embed, Interaction

from hades.globals import gcursor


async def leaderboard(interaction: Interaction):
    embed: Embed = Embed()
    gcursor.execute("""
                    SELECT exp,uid from levels ORDER BY exp DESC;
                    """)
    vals: list[tuple[int, int]] = gcursor.fetchall()
    logger: Logger = logging.getLogger("discord")
    desc: str = ""
    i: int = 1
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("Not in a server")
    else:
        if len(vals) > 10:
            vals = vals[:10]
        for val, uid in vals:
            user = interaction.client.get_user(uid)
            if user is not None:
                desc += f"## {i}. {user.mention} Level {int(val / 100)}\n"
                embed.description = desc
                i += 1
            else:
                logger.error("Found non existent user")
        await interaction.response.send_message(embed=embed)
