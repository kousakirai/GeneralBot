import discord
from discord.ext import commands
import os
from function.help import Help
from models.guild import Guild

class GBot(commands.AutoShardedBot):
    def __init__(self, token):
        self.token = token
        super().__init__(command_prefix=None, help_command=Help(), intents=discord.Intents.all())
        self.load_cogs()

    async def get_prefix(self, message: discord.Message):
        guild = await Guild(message.guild.id).get()
        if guild:
            print("サーバー:", message.guild.name)
            print("接頭文字:", guild.prefix)
            return guild.prefix
        else:
            guild = await Guild.create(message.guild.id)
            guild = await guild.get()
            print("サーバー:", message.guild.name)
            print("接頭文字:", guild.prefix)
            return guild.prefix

    async def on_guild_join(self, guild: discord.Guild):
        guild = await Guild.create(guild.id)
        guild = await guild.get()
        print("サーバー:", guild.name)
        print("接頭文字:", guild.prefix)
    
    def load_cogs(self):
        for filename in os.listdir("cogs"):
            if not filename.startswith("_") and filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")
        self.load_extension("discord_debug")
        self.load_extension("jishaku")
            
    async def on_ready(self):
        print("起動しました")
        #1:Botについて、2:サーバー管理：メンバー、3:娯楽、4:ゲーム


    # 起動用の補助関数です
    def run(self):
        try:
            self.loop.run_until_complete(self.start(self.token))
        except discord.LoginFailure:
            print("Discord Tokenが不正です")
        except KeyboardInterrupt:
            print("終了します")
            self.loop.run_until_complete(self.logout())