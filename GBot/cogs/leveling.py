from discord.ext import commands, tasks
from GBot.core.bot import GBot
from GBot.models.level import Level
import random
import discord
import json


class leveling(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot
        self.update_level.start()

    with open("queue.Json", ) as f:
        data = json.load(f)

    def create_level(self, user_id):
        level = Level.create(user_id=user_id)
        return level.get()

    @tasks.loop(seconds=10)
    async def update_level(self):
        if len(self.data) == 0:
            return
        for user_id in self.data.keys():
            level = Level(user_id).get()
            num = random.randint(0, 5)
            level.set(exp=+num)
            if level.exp > level.level * 6:
                old_level = level.level
                current_level = level.level + 1
                level.set(exp=0, level=current_level)
                embed = discord.Embed(title="レベルが上ったよ！", description=" ")
                name = f"**{old_level}**から{current_level}**になったよ！"
                value = f"次のレベルアップに必要な経験値：{level.level*6}"
                embed.add_field(name=name, value=value)
                channel = self.data.get(user_id).get("message_ch")
                await channel.send(embed=embed)
        print("Levelキュー内の処理を完了しました。")

    @update_level.before_loop
    async def before_printer(self):
        print('Levelキュー待機中...')
        await self.bot.wait_until_ready()
        print('キュー処理開始')

    @commands.Cog.listener()
    async def on_message(self, message):
        level = Level(message.author.id).get()
        if not level:
            level = self.create_level(message.author.id)
        self.data[message.author.id] = {
            "message_ch": message.channel.id,
        }
        with open("queue.Json", mode="w") as f:
            json.dump(self.data, f, indent=4)


def setup(bot):
    return bot.add_cog(leveling(bot))
