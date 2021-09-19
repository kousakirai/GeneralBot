from discord.ext import commands
import discord
from discord.ext.commands.errors import MissingPermissions, MissingRequiredArgument
from GBot.core.bot import GBot
import math
from GBot.models.guild import Guild

class Utils(commands.Cog):
    """Botの設定を変更させる機能のカテゴリです。"""
    def __init__(self, bot: GBot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"現在のレイテンシ：{math.floor(self.bot.latency)}")

    @commands.command(ignore_extra=False)
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: commands.Context, *, prefix: str):
        if len(prefix) > 8:
            return await ctx.send("Prefixは8文字以内である必要があります")
        guild = Guild(ctx.guild.id).get()
        Guild(ctx.guild.id).set(prefix=prefix)
        await ctx.send(f"Prefixを{guild.prefix}から{prefix}に変更しました")

    @prefix.error
    async def on_prefix_error(self, ctx: commands.Context, error):
        if isinstance(error, MissingPermissions):
            return await ctx.send('管理者のみが実行可能です')
        if isinstance(error, MissingRequiredArgument):
            return await ctx.send('引数は新しいPrefixを8文字以内で渡してください')
        raise error

    @commands.command()
    async def about(self, ctx):
        embed = discord.Embed(title="Botの概要", description=" ", colour=discord.Colour.blue())
        embed.add_field(name="前置き", value="このBotは個人が制作しています。\nバグなども多数ありますが発見した際には下のサポートサーバーで\\nご一報いただけるとすぐさま対応いたします。")
        embed.add_field(name="Bot稼働状態", value="[こちら](https://stats.uptimerobot.com/rVZNriABK4)のサイトからBotの稼働状態が確認できます。\n緑のランプが付いているときは正常です。")
        embed.add_field(name="サポートサーバー", value="[こちら](https://discord.gg/feudwTMnEd)", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    return bot.add_cog(Utils(bot))
