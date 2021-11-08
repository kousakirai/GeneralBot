from GBot.core.bot import GBot
import os
from GBot.db import DB

DB.engine()
GBot(
    os.environ["CANARYBOT_TOKEN"]
    ).run()
