import discord
from discord.ext import commands
from GBot.core.bot import GBot


class invites(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot
    """
    @commands.command()
    async def invite(self, ctx):
        guild = ctx.guild
        invites = await guild.invites()

        for invite in invites:
            if invite.inviter.id == ctx.author.id:
                for member in guild.members:
                    if invite.target_user.name == member.name:
    """

def setup(bot):
    return bot.add_cog(invites(bot))