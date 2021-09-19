from discord.ext import commands
from GBot.core.bot import GBot


class Joke(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot

    @commands.command(name="gold")
    async def _gold(self, ctx, Quantity):
        await ctx.send(f"金塊を{Quantity}個生成しました。")

    @commands.command(name="JS")
    async def _JS(self, ctx):
        await ctx.send(f"{ctx.author.mention}JS最強！")


def setup(bot):
    return bot.add_cog(Joke(bot))
