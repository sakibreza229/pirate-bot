# main.py
import os
import asyncio
import logging
from discord.ext import commands
from data import DataManager
from utils import INTENTS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Modules to load
MODULES = [
    "commands.inquire",
    "commands.loot",
    "commands.shop",
    "commands.balance",
    "commands.inventory",
    "commands.leaderboard",
    "commands.missions",
    "commands.daily_weekly",
    "commands.stats_help",
    "commands.ahoy",
]

logging.basicConfig(level=logging.INFO)

async def main():
    # Create bot
    bot = commands.Bot(command_prefix="!", intents=INTENTS)
    bot.remove_command("help")

    # Create data manager
    data = DataManager("pirate_data.json")

    # Load modules
    for mod in MODULES:
        logging.info(f"Loading module: {mod}")
        module = __import__(mod, fromlist=["setup"])
        setup = getattr(module, "setup", None)
        if setup:
            await setup(bot, data)
        else:
            logging.warning(f"No setup() in {mod}")

    # Sync commands on startup
    @bot.event
    async def on_ready():
        logging.info(f"Logged in as {bot.user} (id: {bot.user.id})")
        try:
            await bot.tree.sync()
            logging.info("Slash commands synced.")
        except Exception as e:
            logging.exception("Failed to sync commands: %s", e)

    # Get token from environment
    TOKEN = os.getenv("PIRATE_BOT_TOKEN")
    if not TOKEN:
        raise RuntimeError("Please set PIRATE_BOT_TOKEN in environment variables.")

    # Run bot
    await bot.start(TOKEN)

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
    
