import csv
import io
import logging
import os

from discord import File, Interaction, Member
from discord.channel import ForumChannel


async def auditions_csv(interaction: Interaction) -> None:
    logger = logging.getLogger("discord")
    await interaction.response.defer(ephemeral=True)

    adminid = int(os.getenv("ADMINROLEID") or "-1")
    modid = int(os.getenv("MODROLEID") or "-1")
    if adminid == -1:
        logger.error("ADMINROLEID not set!")
        return await interaction.followup.send("Internal error, try again later")
    if modid == -1:
        logger.error("MODROLEID not set!")
        return await interaction.followup.send("Internal error, try again later")

    if not isinstance(interaction.user, Member):
        return await interaction.followup.send("This command can only be used in a server")

    user_roles = [r.id for r in interaction.user.roles]
    if modid not in user_roles and adminid not in user_roles:
        return await interaction.followup.send("You don't have perms for this!")

    guild = interaction.guild
    if guild is None:
        return await interaction.followup.send("Not in a server")

    audchannelid = os.getenv("AUDCHANNELID") or "-1"
    channel = await guild.fetch_channel(int(audchannelid))
    if not isinstance(channel, ForumChannel):
        return await interaction.followup.send("Audition forum channel not found")

    threads = list(channel.threads)
    async for t in channel.archived_threads(limit=None):
        threads.append(t)

    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["username", "roles", "thread_title"])

    for thread in threads:
        starter = thread.owner
        username = starter.name if starter is not None else ""
        roles = "; ".join(tag.name for tag in thread.applied_tags)
        writer.writerow([username, roles, thread.name])

    buffer.seek(0)
    data = buffer.getvalue().encode("utf-8")
    file = File(io.BytesIO(data), filename="auditions.csv")
    await interaction.followup.send(file=file)
