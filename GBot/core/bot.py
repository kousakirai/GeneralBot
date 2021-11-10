import discord
from discord.ext import commands
import os
from GBot.function.help import Help
from GBot.models.guild import Guild
from GBot.data import data
from discord.ext.commands.errors import (
    CommandNotFound,
    MissingPermissions,
    BadArgument,
    NotOwner
)
import traceback
from GBot.db import DB

class GBot(commands.Bot):
    def __init__(self, token):
        self.token = token
        super().__init__(command_prefix=None, help_command=Help())

    async def is_owner(self, user: discord.User):
        if user.id in data["team_id"]:
            return True
        return await super().is_owner(user)

    async def get_prefix(self, message: discord.Message):
        guild = Guild(message.guild.id).get()
        if guild:
            if self.user.id == 899076159604686850:
                print("サーバー:", message.guild.name)
                print("接頭文字:", guild.prefix)
                print("認証：", str(guild.auth))
                print("レベル", str(guild.level))
                return "gc!"
            elif guild.auth is None:
                print("サーバー:", message.guild.name)
                print("接頭文字:", guild.prefix)
                print("認証：", str(guild.auth))
                print("レベル", str(guild.level))
                return guild.prefix
            else:
                print("サーバー:", message.guild.name)
                print("接頭文字:", guild.prefix)
                print("認証：", str(guild.auth))
                print("レベル", str(guild.level))
                return guild.prefix
        else:
            guild = Guild.create(guild_id=message.guild.id)
            print(guild)
            guild = guild.get()
            if guild.level is None:
                print("サーバー:", message.guild.name)
                print("接頭文字:", guild.prefix)
                print("認証：", str(guild.auth))
                print("レベル", str(guild.level))
                return guild.prefix
            print("サーバー:", message.guild.name)
            print("接頭文字:", guild.prefix)
            print("認証：", str(guild.auth))
            print("レベル", str(guild.level))
            return guild.prefix

    async def on_guild_join(self, guild: discord.Guild):
        guild = Guild.create(guild_id=guild.id)
        guild = guild.get()
        print("サーバー:", guild.name)
        print("接頭文字:", guild.prefix)
        print("認証：", str(guild.auth))
        print("レベル：", str(guild.level))

    async def on_command_error(self, ctx, error):
        guild = Guild(ctx.guild.id).get()
        embed = discord.Embed(
            title="エラー", description=" ",
            color=discord.Color.red()
            )

        if isinstance(error, CommandNotFound):
            embed.add_field(
                name="コマンドが存在しません。",
                value=f"`{guild.prefix}help`を実行してコマンドリストを確認してください。"
                )

        elif isinstance(error, MissingPermissions):
            embed.color = data["color"]["red"]
            embed.add_field(
                name="権限エラー",
                value="実行者とBotの権限をお確かめください。"
                )

        elif isinstance(error, BadArgument):
            embed.color = data["color"]["purple"]
            embed.add_field(
                name="引数エラー",
                value="引数が不正もしくは不足しています。"
                )

        elif isinstance(error, NotOwner):
            embed.add_field(
                name="devコマンド",
                value="このコマンドは運営のみ使用可能です。"
                )

        else:
            print(error)
            channel = self.get_channel(data["devch"])
            embed.title = "未知のエラー"
            embed.description = " "
            embed.add_field(name=error, value="エラーを修正してください。")
            await channel.send(embed=embed)
        return await ctx.send(embed=embed)

    async def on_ready(self):
        for filename in os.listdir("GBot/cogs"):
            if not filename.startswith("_") and filename.endswith(".py"):
                self.load_extension(f"GBot.cogs.{filename[:-3]}")
                print(f"{filename[:-3]}をロード")
        self.load_extension("jishaku")

    def run(self):
        try:
            self.loop.run_until_complete(
                self.start(self.token)
                )
        except discord.LoginFailure:
            print("Discord Tokenが不正です")
        except KeyboardInterrupt:
            print("終了します")
            self.loop.run_until_complete(self.close())
            DB.close(self)
        except Exception:
            traceback.print_exc()
