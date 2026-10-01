import logging
from random import randint

from discord import ClientUser, Member, Message, Role

import hades.globals as globa
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
    gcursor.execute(
        """
    SELECT exp FROM levels WHERE uid = ?;
    """,
        [uid],
    )
    res = gcursor.fetchone()
    if isinstance(message.author, Member):
        roles: list[Role] = message.author.roles  # pyright: ignore[reportUnknownVariableType]
        if res is not None:
            if isinstance(res[0], int):
                exp = int((res[0] // 500) * 500)
                lvl = int((exp / 500) * 5)
                print(f"current level: {lvl}")
                if lvl < 1:
                    print("lvl < 1")
                    return
                else:
                    for r in roles:
                        if r.name == f"Level {lvl - 5}":
                            print(f"trying to add Level {lvl - 5}")
                            await message.author.remove_roles(r)
                    g = message.guild
                    if g is not None:
                        rx = globa.getrole(lvl, g)
                        await message.author.add_roles(rx)
                        x = message.author.roles
                        print(f"new roles: {x}")
