import discord
from discord.ext import commands
import random
from GBot.core.bot import GBot

class leveling(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot


def setup(bot):
    return bot.add_cog(leveling(bot))
