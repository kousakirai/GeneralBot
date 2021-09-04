from discord.ext import commands
from core.bot import GBot
from discord_slash import cog_ext, SlashContext


class Joke(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot

    @cog_ext.cog_slash(name="gold")
    async def _gold(self, ctx: SlashContext, Quantity):
        await ctx.send(f"金塊を{Quantity}個生成しました。")

    @cog_ext.cog_slash(name="JS")
    async def _JS(self, ctx: SlashContext):
        await ctx.send(f"{ctx.author.mention}JS最強！")


def setup(bot):
    return bot.add_cog(Joke(bot))
