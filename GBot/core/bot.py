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
from sanic import Sanic
from sanic.response import text
from sanic.log import logger


class GBot(commands.Bot):
    def __init__(self, token):
        self.token = token
        self.app = Sanic("Generalbot")
        self.app.register_listener(self.setup, "main_process_start")
        self.app.register_listener(self.stop, "before_server_stop")

    async def is_owner(self, user: discord.User):
        if user.id in data["team_id"]:
            return True
        return await super().is_owner(user)

    async def get_prefix(self, message: discord.Message):
        guild = Guild(message.guild.id).get()
        if guild:
            if guild.auth is None:
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
        print("レベル", str(guild.level))

    async def on_command_error(self, ctx, error):
        guild = Guild(ctx.guild.id).get()
        embed = discord.Embed(title="エラー", description=" ",
                              color=discord.Color.red())

        if isinstance(error, CommandNotFound):
            embed.add_field(name="コマンドが存在しません。",
                            value=f"`{guild.prefix}help`を実行してコマンドリストを確認してください。"
                            )

        elif isinstance(error, MissingPermissions):
            embed.color = data["color"]["red"]
            embed.add_field(name="権限エラー", value="実行者とBotの権限をお確かめください。")

        elif isinstance(error, BadArgument):
            embed.color = data["color"]["purple"]
            embed.add_field(name="引数エラー", value="引数が不正もしくは不足しています。")

        elif isinstance(error, NotOwner):
            embed.add_field(name="devコマンド", value="このコマンドは運営のみ使用可能です。")

        else:
            print(error)
            channel = self.bot.get_channel(data["devch"])
            embed.title = "未知のエラー"
            embed.description = " "
            embed.add_field(name=error, value="エラーを修正してください。")
            return await channel.send(embed=embed)
        await ctx.send(embed=embed)

    async def on_ready(self):
        for filename in os.listdir("GBot/cogs"):
            if not filename.startswith("_") and filename.endswith(".py"):
                self.load_extension(f"GBot.cogs.{filename[:-3]}")
                print(f"{filename[:-3]}をロード")
        self.load_extension("jishaku")
        logger.info("Bot online")

    async def setup(self, app, loop):
        @self.app.route('/')
        async def main(request):
            return text("Alive")

        intents = discord.Intents.all()
        intents.typing = False
        super().__init__(command_prefix=None,
                         intents=intents,
                         help_command=Help()
                         )
        loop.create_task(self.start(self.token))
        await self.wait_until_ready()
        logger.info("starting...")

    async def stop(self, app, loop):
        logger.info("shutdown...")
        await self.close()

    def run(self):
        self.app.run(host="0.0.0.0", port=8080)
