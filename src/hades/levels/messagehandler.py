import logging

from discord import ClientUser, Member, Message, User
from hades.globals import gcursor
from random import randint

async def msghandler(user: ClientUser | None, message: Message):
    if user is None:
        return
    logger = logging.getLogger("discord")
    if message.author == user:
        # ignore self messages
        return
    uid = message.author.id
    logger.info(f"{message.author.name} talked")
    gcursor.execute("""
    UPDATE levels SET exp = exp + ? WHERE uid = ?;
    """, [randint(1,10),uid])
