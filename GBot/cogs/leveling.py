from discord.ext import commands, tasks
from GBot.core.bot import GBot
from GBot.models.level import Level
import random
import discord
import json


class leveling(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot


def setup(bot):
    return bot.add_cog(leveling(bot))
