from discord.ext import commands
import discord
from GBot.models.GBan import GBan


class Gbansys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def setup(self, ctx):
        await ctx.send("Grobal Banのセットアップが開始されました。\n本当に実行しますか？")


def setup(bot):
    return bot.add_cog(Gbansys(bot))
