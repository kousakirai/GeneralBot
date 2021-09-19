from GBot.core.bot import GBot
import os
from keep_alive import keep_run
from GBot.db import DB
DB.engine()
GBot(os.environ["BOT_TOKEN"]).run()
keep_run()