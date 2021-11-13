from GBot.core.bot import GBot
import os
from GBot.db import DB

DB.engine()
GBot(
    os.getenv("CANARYBOT_TOKEN")
    ).run()
