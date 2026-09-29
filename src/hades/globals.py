import os
from sqlite3 import Cursor, connect
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) 
pathToDB = os.getenv("LEVELSDBFILEPATH") or "NoDB"

gcursor = None

if pathToDB == "NoDB":
    raise RuntimeError("LEVELSDBFILEPATH is not set!")
else:
    db = Path(pathToDB)
    if db.exists():
        conn = connect(db)
        gcursor = conn.cursor()
    else:
        db.touch()
        conn = connect(db)
        gcursor = conn.cursor()
