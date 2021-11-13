from discord.ext import commands, tasks
from GBot.core.bot import GBot
from GBot.models.level import Level
import random
import discord
from GBot.models.guild import Guild
from GBot.data import data

from dataclasses import dataclass


@dataclass
class LevelQueueEntry:
    user_id: int
    channel_id: int
    guild_id: int

class leveling(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot
        self.Lqueue.start()
        self.queue = []

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()
        user_id = message.author.id
        channel_id = message.channel.id
        guild_id = message.guild.id
        self.queue.append(LevelQueueEntry(user_id, channel_id, guild_id))

    @tasks.loop(seconds=5)
    async def Lqueue(self):
        print(self.queue)
        if len(self.queue) == 0:
            return
        LQE = self.queue[0]
        user_id = LQE.user_id
        print(user_id)
        guild = Guild(LQE.guild_id).get()
        level = Level(
            user_id
        ).get()
        if level:
            num = random.randint(
                1,
                5
            )
            exp = level.exp + num
            Level(
                user_id
            ).set(
                exp=exp
            )
            if level.exp > level.level * guild.level_exp:
                level = level.level + 1
                Level(
                    user_id
                ).set(
                    level=level,
                    exp=0
                )
                user = self.bot.get_user(
                    user_id
                )
                embed = discord.Embed(
                    title="レベルアップ！",
                    description=" ",
                    colour=data["color"]["green"]
                )
                embed.add_field(
                    name=f"{user.name}さんのレベルが{level.level}に上がったよ！",
                    value=f"次のレベルアップに必要な経験値：{level.level*6}"
                )
                channel = self.bot.get_channel(LQE.message_id)
                await channel.send(embed=embed)
                self.queue.pop(0)
            else:
                self.queue.pop(0)
                return
        else:
            self.queue.pop(0)
            return

    @Lqueue.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.Lself.queue.cancel()

    @commands.group()
    async def level(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @level.command()
    async def check(self, ctx):
        level = Level(ctx.author.id).get()
        if level:
            embed = discord.Embed(
                title=f"{ctx.author.name}さんの現在のレベル",
                description=" ",
                colour=data["color"]["purple"]
            )
            embed.add_field(
                name=f"レベル：**{level.level}",
                value="この調子でGo！Go！"
            )
            embed.add_field(
                name=f"現在の経験値：__{level.exp}__",
                value=f"次のレベルアップまでに必要な経験値：{level.level*6 - level.exp}"
            )
            await ctx.reply(embed=embed)

    @level.command(alias=["at"])
    async def Activite(self, ctx):
        guild = Guild(ctx.guild.id).get()
        if guild.level is True:
            Guild(ctx.guild.id).set(level=False)
            await ctx.reply("レベル機能をこのサーバーで無効化しました。")
        elif guild.level is False:
            Guild(ctx.guild.id).set(level=True)
            await ctx.reply(
                """
                レベル機能をこのサーバーで有効化しました。
                \n経験値の上限倍率：現在のレベル×6
                \n経験値上昇の間隔：1～5
                """
            )

    @level.command()
    async def exp_set(self, ctx, exp):
        guild = Guild(
            ctx.guild.id
        ).get()

        Guild(
            ctx.guild.id
        ).set(
            Level_exp=exp
        )
        await ctx.reply(f"倍率を{guild.level_exp}から{exp}に変更しました。")

    @level.command()
    async def width_set(self, ctx, width):
        guild = Guild(
            ctx.guild.id
        ).get()

        Guild(
            ctx.guild.id
        ).set(
            level_width=width
        )

        await ctx.reply(f"経験値の範囲を{guild.level_width}から{width}に変更しました。")

def setup(bot):
    return bot.add_cog(
        leveling(
            bot
        )
    )
