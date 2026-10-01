import os
from pathlib import Path
from sqlite3 import connect

import discord
from discord import Guild, Role
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
pathtodb = os.getenv("LEVELSDBFILEPATH") or "NoDB"

gcursor = None


files: str | None = os.getenv("FILESGENPATH")
if files is None:
    raise RuntimeError("FILESGENPATH not set!")
else:
    filespath: Path = Path(files)
    if not filespath.exists():
        filespath.mkdir()

if pathtodb == "NoDB":
    raise RuntimeError("LEVELSDBFILEPATH is not set!")
else:
    db = Path(pathtodb)
    if db.exists():
        conn = connect(db)
        gcursor = conn.cursor()
    else:
        db.touch()
        conn = connect(db)
        gcursor = conn.cursor()


def getrole(lvl: int, guild: Guild) -> Role:
    x = discord.utils.get(guild.roles, name=f"Level {lvl}")
    if x is not None:
        return x
    else:
        raise RuntimeError(f"Tried to find role for invalid level {lvl}")
