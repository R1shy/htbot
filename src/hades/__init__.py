import logging
import os

from discord import Intents, Interaction, Member, Message, Object
from discord.ext.commands import Bot  # pyright: ignore

from hades.audcount import audcount
from hades.evilfaq import evilfaq
from hades.faq import faq
from hades.globals import gcursor
from hades.levels.getlevel import gl 
from hades.levels.givexp import ge
from hades.levels.leaderboard import leaderboard
from hades.levels.messagehandler import msghandler
from hades.scrapejoin import sj
intents = Intents.all()
bot = Bot(command_prefix="?", intents=intents)
global botuser
botuser = bot.user


@bot.event
async def on_ready():
    gcursor.execute("""
                    CREATE TABLE IF NOT EXISTS levels (
                    uid INTEGER UNIQUE PRIMARY KEY NOT NULL,
                    name TEXT UNIQUE NOT NULL,
                    exp INTEGER NOT NULL DEFAULT 0
                    );
                    """)
    logger = logging.getLogger("discord")
    logger.setLevel(logging.WARNING)
    logger.info(f"Logged in as {bot.user}")

    try:
        z = os.getenv("SERVERID") or ""
        bot.tree.copy_global_to(guild=Object(id=z))
        synced = await bot.tree.sync(guild=Object(id=z))
        logger.info(f"Successfully synced {len(synced)} slash command(s).")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")


@bot.tree.command(name="ping", description="Responds with a pong!")
async def meow(interaction: Interaction):
    await interaction.response.send_message("pong")


@bot.tree.command(name="scrapejoins", description="scrape joins into a csv")
async def scrape_joins(interaction: Interaction):
    await sj(interaction)


@bot.tree.command(name="numberofauditions", description="get the number of auditions")
async def ac(interaction: Interaction):
    await audcount(interaction)


@bot.tree.command(name="faq", description="Frequently Asked Questions")
async def faaq(interaction: Interaction):
    await faq(interaction)


@bot.tree.command(name="evilfaq", description="Evil Frequently Asked Questions")
async def efaq(interaction: Interaction):
    await evilfaq(interaction)


@bot.tree.command(name="getlevel", description="Get your level")
async def getlevel(interaction: Interaction):
    await gl(interaction)


@bot.tree.command(name="giveexp", description="Give someone exp, staff ONLY")
async def givexp(interaction: Interaction, addamount: int, member: Member):
    await ge(interaction, addamount, member)


@bot.tree.command(name="leaderboard", description="Leaderboard of levels")
async def lb(interaction: Interaction):
    await leaderboard(interaction)


@bot.event
async def on_message(message: Message):
    await msghandler(bot.user, message)


def main() -> None:
    files = os.getenv("FILESGENPATH") or "NoFiles"
    if files == "NoFiles":
        logging.getLogger("discord").warning(
            "FILESEGENPATH not set, falling back to $HOME"
        )
        files = os.getenv("HOME") or "NoHome"
        if files == "NoHome":
            raise RuntimeError("FILESGENPATH and $HOME are not set!")

    x = os.getenv("DISCTOKEN")
    if x is not None:
        bot.run(x)
    else:
        raise RuntimeError("DISCTOKEN not set!")


if __name__ == "__main__":
    main()
