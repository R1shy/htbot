import csv
from datetime import datetime
import os
from discord import Intents, Interaction, Object, TextChannel
from discord.ext.commands import Bot                                                                                                                                                                  
from dotenv import load_dotenv, find_dotenv
from csv import writer

from scrapymcscrapeface.audcount import audcount
from scrapymcscrapeface.scrapejoin import sj

load_dotenv(find_dotenv()) 
intents = Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

bot = Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        z = os.getenv("SERVERID") or ""
        bot.tree.copy_global_to(guild=Object(id=z))
        synced = await bot.tree.sync(guild=Object(id=z))
        print(f"Successfully synced {len(synced)} slash command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="ping", description="Responds with a pong!")
async def meow(interaction: Interaction):
    await interaction.response.send_message("pong")

@bot.tree.command(name="scrapejoins", description="scrape joins into a csv")
async def scrape_joins(interaction: Interaction):
    await sj(interaction)

@bot.tree.command(name="numberofauditions", description="get the number of auditions")
async def ac(interaction: Interaction):
    await audcount(interaction)

def main() -> None:
    x = os.getenv("DISCTOKEN")
    if x is not None:
        bot.run(x)
    else:
        raise RuntimeError("No token :(")

if __name__ == "__main__":
    main()
