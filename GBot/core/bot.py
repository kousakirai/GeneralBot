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
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands
from logging import getLogger

import traceback
from GBot.db import DB
intents = discord.Intents.all()
intents.typing = False
intents.voice_states = False
intents.presences = False
LOG = getLogger(__name__)


class GBot(commands.Bot):
    def __init__(self, token):
        self.token = token
        super().__init__(
            command_prefix=None,
            help_command=Help(),
            intents=intents
            )
        mongo_db = DB.start()
        # スラッシュコマンドオブジェクトのインスタンス
        slash = SlashCommand(self, sync_commands = True, override_type = True)
        guild_ids = [878265923709075486]

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
        await self.bot.change_presence(name="waiting...", type=discord.ActivityType.custom)
        self.load_extension("jishaku")
        for filename in os.listdir("GBot/cogs"):
            if not filename.startswith("_") and filename.endswith(".py"):
                self.load_extension(f"GBot.cogs.{filename[:-3]}")
                LOG.info(f"{filename[:-3]}をロード")
        LOG.info('We have logged in as {0.user}'.format(self))
        LOG.info(f'### guilds ### \n{self.guilds}')
        LOG.info('bot ready.')
        activity = discord.Activity(name = '現在稼働中', type = discord.ActivityType.watching)
        await self.change_presence(activity=activity)
        BOT_USER_ID = GBot.user.id
        DISCORD_TOKEN = self.token
        GUILD_ID = 878265923709075486
        cmds = await manage_commands.get_all_commands(BOT_USER_ID, DISCORD_TOKEN, GUILD_ID)
        for cmd in cmds:
            LOG.info(cmd)

    def run(self):
        try:
            self.loop.run_until_complete(
                self.start(self.token)
                )
        except discord.LoginFailure:
            LOG.info("Discord Tokenが不正です")
        except KeyboardInterrupt:
            LOG.info("終了します")
            self.loop.run_until_complete(self.close())
            DB.close(mongo_db)
        except Exception:
            traceback.print_exc()
