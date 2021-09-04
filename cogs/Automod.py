import discord
from discord.ext import commands
from core.bot import GBot
import asyncio


class Automod(commands.Cog):
    """サーバーの管理を簡略化するための機能です。"""
    def __init__(self, bot: GBot):
        self.bot = bot

    @commands.group(brief=2)
    async def Auto(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("引数・コマンドが不正です。")

    @Auto.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member, mute_time: int = 300):
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name="Muted")
        if role == None:
            await guild.create_role(name="Muted")
            role = discord.utils.get(guild.roles, name="Muted")
            permissions = role.permissions
            permissions.send_message = False
            await role.edit(permissions=permissions)
        for channel in guild.channels:
            await channel.set_permissions(role, send_messages=False)
        await user.add_roles(role)
        embed = discord.Embed(title=f"✅ __{user.name}__をミュートしました",
                              description=" ",
                              color=0x87CEFA)
        await ctx.send(f'{user.mention}', embed=embed)
        await asyncio.sleep(mute_time)
        await user.remove_roles(role)
        await ctx.send(f"{user.name}のミュートが終了しました。")

    @Auto.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, reason=None):
        guild = ctx.guild
        member = discord.utils.get(guild.members, name=user.name)
        await member.kick()
        embed = discord.Embed(title=f"✅ __{user.name}__をキックしました",
                              description=" ",
                              color=0x87CEFA)
        await ctx.send(embed=embed)

    @Auto.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, reason=None):
        guild = ctx.guild
        member = discord.utils.get(guild.members, name=user.name)
        await member.ban()
        embed = discord.Embed(title=f"__{user.name}__をバンしました。",
                              description=" ",
                              color=0x87CEFA)
        await ctx.send(embed=embed)


def setup(bot):
    return bot.add_cog(Automod(bot))
