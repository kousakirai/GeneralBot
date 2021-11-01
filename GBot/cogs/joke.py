from discord.ext import commands
from GBot.core.bot import GBot


class Joke(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot


def setup(bot):
    return bot.add_cog(Joke(bot))
