from GBot.core.bot import GBot
import os

GBot(
    os.getenv("BOT_TOKEN")
    ).run()
