from discord.ext import commands
from GBot.core.bot import GBot
from logging import getLogger
from discord_slash import cog_ext, SlashContext
from discord_slash.utils import manage_commands
from discord_slash.model import SlashCommandOptionType
LOG = getLogger(__name__)
class Joke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        LOG.info('constructor end')

    guild_ids = GBot.guild_ids
    test_options = [
        manage_commands.create_option(
            name = 'num',
            description = '個数指定',
            option_type = SlashCommandOptionType.STRING, # 3
            required = True
            ),
        ]

    def cog_unload(self):
        return super().cog_unload()

    @cog_ext.cog_slash(
        name = 'gold', description = '金を生成できます。',
        options = test_options, guild_ids = guild_ids
                    )
    async def _test(self, ctx: SlashContext, param: str = None):
        message='{0}個の金を生成しました。'.format(param)
        await ctx.send(message)

def setup(bot):
    return bot.add_cog(
        Joke(
            bot
            )
        )
