from discord.ext import commands
import discord
from discord.ext.commands.errors import (
    MissingPermissions,
    MissingRequiredArgument
)

from GBot.core.bot import GBot
from GBot.models.guild import Guild
from time import monotonic


async def reply(message):
    guild = Guild(message.guild.id).get()
    reply = f'{message.author.mention} プレフィックスは`{guild.prefix}`です。'
    await message.channel.send(reply)


class Utils(commands.Cog):
    """Botの設定を変更させる機能のカテゴリです。"""

    def __init__(self, bot: GBot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        # Δt = t1 - t0 の t0 を定義する。
        t0 = monotonic()
        # Discord を通す関数を挟む。(応答速度)
        embed = discord.Embed(title="計算中...", description=' ')
        ping_message = await ctx.send(embed=embed)

        # Δt = t1 - t0, latency は ping 的な意味、応答速度。1000倍は、ms(ミリセカンド)にするため。
        latency = (monotonic() - t0) * 1000

        # 送っていたメッセージを編集。ここで、応答速度を表示する。int にしているのは、小数点を消すため。( int は整数値)
        title = f"Pong! 応答速度**{int(latency)}** ms です。"
        color = discord.Color.random()
        await ping_message.edit(embed=discord.Embed(title=title, color=color))

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
        if isinstance(
            error,
            MissingPermissions
        ):
            return await ctx.send(
                '管理者のみが実行可能です'
            )
        if isinstance(
            error,
            MissingRequiredArgument
        ):

            return await ctx.send(
                '引数は新しいPrefixを8文字以内で渡してください'
            )
        raise error

    @commands.command()
    async def about(self, ctx):
        url = "[こちら](https://stats.uptimerobot.com/rVZNriABK4)"
        message = "\nご一報いただけるとすぐさま対応いたします。"
        embed = discord.Embed(
            title="Botの概要", description=" ",
            colour=discord.Colour.blue()
        )

        embed.add_field(
            name="前置き",
            value="このBotは個人が制作しています。\nバグなども多数ありますが発見した際には下のサポートサーバーで"+message
        )

        embed.add_field(
            name="Bot稼働状態",
            value=url+"のサイトからBotの稼働状態が確認できます。\n緑のランプが付いているときは正常です。"
        )

        embed.add_field(
            name="サポートサーバー",
            value="[こちら](https://discord.gg/feudwTMnEd)",
            inline=False
        )
        await ctx.send(
            embed=embed
        )

    # 発言時に実行されるイベントハンドラを定義
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:  # 話しかけられたかの判定
            await reply(
                message
            )  # 返信する非同期関数を実行


def setup(bot):
    return bot.add_cog(
        Utils(
            bot
        )
    )
