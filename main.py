from core.bot import GBot
import os
from keep_alive import keep_alive

keep_alive()
GBot(os.environ["BOT_TOKEN"]).run()