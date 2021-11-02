from discord.ext import commands, tasks
from GBot.core.bot import GBot
from GBot.models.level import Level
import random


class leveling(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot

    async def create_level(self, user_id):
        num = random.randint(0, 5)
        level = Level.create(user_id=user_id)
        level = level.get()
        level.set(exp=num)

    @tasks.loop(seconds=60)
    async def update_level(self, user_id):
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        level = Level(message.author.id).get()
        if level < 0:
            return


def setup(bot):
    return bot.add_cog(leveling(bot))
