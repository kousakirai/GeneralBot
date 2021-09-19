import discord
from discord.ext import commands
import os
from GBot.function.help import Help
from GBot.models.guild import Guild


class GBot(commands.AutoShardedBot):
    def __init__(self, token):
        self.token = token
        super().__init__(command_prefix=None, intents=discord.Intents.all(),
        help_command=Help())
        self.load_cogs()

    async def get_prefix(self, message : discord.Message):
        guild = Guild(message.guild.id).get()
        if guild:
            print(f"サーバー名：{message.guild.name}")
            print(f"接頭文字：{guild.prefix}")
            return guild.prefix
        else:
            guild = Guild.create(guild_id=message.guild.id)
            print(guild)
            guild = guild.get()
            print("サーバー:", message.guild.name)
            print("接頭文字:", guild.prefix)
            return guild.prefix
    
    async def on_guild_join(self, guild: discord.Guild):
        guild = Guild.create(guild_id=guild.id)
        guild = guild.get()
        print("サーバー:", guild.name)
        print("接頭文字:", guild.prefix)

    def load_cogs(self):
        for filename in os.listdir("GBot/cogs"):
            if not filename.startswith("_") and filename.endswith(".py"):
                self.load_extension(f"GBot.cogs.{filename[:-3]}")
        self.load_extension("jishaku")
        
    async def on_ready(self):
        print("起動しました")

    # 起動用の補助関数です
    def run(self):
        try:
            self.loop.run_until_complete(self.start(self.token))
        except discord.LoginFailure:
            print("Discord Tokenが不正です")
        except KeyboardInterrupt:
            print("終了します")
            self.loop.run_until_complete(self.logout())