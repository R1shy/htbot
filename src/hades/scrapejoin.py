import csv
import os
from datetime import datetime

from aiofiles import open
from discord import Interaction, TextChannel

path = os.getenv("FILESGENPATH") or os.getenv("HOME") or ""

async def sj(interaction: Interaction):
    g = interaction.guild
    if g is None:
        return await interaction.response.send_message("Not in a server")

    await interaction.response.defer(ephemeral=True)

    name = f"joinsat{int(datetime.now().timestamp())}.csv"
    channel_id = int(os.getenv("JOINS") or -1)
    c = g.get_channel(channel_id)

    if c is None or not isinstance(c, TextChannel):
        print(type(c))
        return await interaction.followup.send("Target text channel not found.")

    async with open(path + "/" + name, "x", newline="") as f:
        w = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(["created_at_day_of_year", "created_at_24_hour_time", "created_at_epoch_seconds", "message_author"])

        seen = set()
        async for msg in c.history(limit=None, oldest_first=True):
            if msg.content == "" and msg.author.name not in seen:
                t: datetime = msg.created_at
                day = t.strftime("%m-%d")
                hour = t.strftime("%H:%M")
                d = [day, hour, int(msg.created_at.timestamp()), msg.author.name]
                seen.add(msg.author.name)
                w.writerow(d)
    await interaction.followup.send(f"Successfully created {name}")
