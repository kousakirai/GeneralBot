# RT Ext - Debug

from discord.ext import commands, tasks
import discord

from jishaku.functools import executor_function
import psutil
from GBot.core.bot import GBot


class monitor(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot

    @executor_function
    def make_monitor_embed(self):
        embed = discord.Embed(
            title="GBot-run info",
            description="Running on Linux",
            color=0x0066ff
        )
        embed.add_field(
            name="Memory",
            value=f"{psutil.virtual_memory().percent}%"
        )
        embed.add_field(
            name="CPU",
            value=f"{psutil.cpu_percent(interval=1)}%"
        )
        embed.add_field(
            name="Disk",
            value=f"{psutil.disk_usage('/').percent}%"
        )
        return embed

    @tasks.loop(minutes=1)
    async def monitor(self):
        await self.make_monitor_embed()


def setup(bot):
    bot.add_cog(
        monitor(
            bot
        )
    )
