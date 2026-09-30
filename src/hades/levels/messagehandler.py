import logging
from random import randint

from discord import ClientUser, Message

from hades.globals import gcursor


async def msghandler(user: ClientUser | None, message: Message):
    if user is None:
        return
    logger = logging.getLogger("discord")
    gcursor.execute(
        """
                    SELECT exp FROM levels WHERE uid = ?;
                    """,
        [message.author.id],
    )
    if gcursor.fetchone() is None:
        # insert new person to back fill
        gcursor.execute(
            """
                        INSERT INTO levels (uid, name, exp) VALUES (?,?,0);
                        """,
            [message.author.id, message.author.name],
        )
        gcursor.connection.commit()
    if message.author == user:
        return
    uid = message.author.id
    logger.info(f"{message.author.name} talked")
    gcursor.execute(
        """
    UPDATE levels SET exp = exp + ? WHERE uid = ?;
    """,
        [randint(1, 10), uid],
    )
    gcursor.connection.commit()
