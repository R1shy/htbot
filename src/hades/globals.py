import os
from pathlib import Path
from sqlite3 import connect

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
pathtodb = os.getenv("LEVELSDBFILEPATH") or "NoDB"

gcursor = None

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
