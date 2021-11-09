from discord.ext import commands
from GBot.core.bot import GBot


class afk(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot

    @commands.command(name='afk')
    async def afk(self,ctx,reason):
        await ctx.send(reason)

def setup(bot):
    return bot.add_cog(
        afk(
            bot
            )
        )