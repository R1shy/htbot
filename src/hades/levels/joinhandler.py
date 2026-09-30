import logging

from discord import Member

from hades.globals import gcursor


async def omj(member: Member):
    logger = logging.getLogger("discord")
    try:
        gcursor.execute("""
        INSERT INTO levels (uid,name,exp) VALUES (?,?,0);
        """,
            [member._user.id,member.name])
    except Exception as e:
        logger.error(str(e))

