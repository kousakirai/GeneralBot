from core.bot import GBot
import os
from keep_alive import keep_alive
import subprocess
import sys
from discord_slash import SlashCommand, SlashContext

alem = subprocess.Popen("pip install alembic;cd alembic;alembic upgrade head;alembic revision --autogenerate;alembic upgrade head;cd ..", shell=True, stdout=sys.stdout, stderr=sys.stdout, text=True)

res = alem.communicate()
# サブプロセスの完了を待つ
# ここではsleepしている60秒待たされる
SlashCommand(GBot)
keep_alive()
GBot(os.environ["BOT_TOKEN"]).run()