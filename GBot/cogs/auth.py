import discord
from discord.ext import commands
from GBot.core.bot import GBot
from GBot.models.auth import Auth
from captcha.image import ImageCaptcha
import random
from GBot.models.guild import Guild


class Authsys(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = Guild(
            member.guild.id
            ).get()
        if not guild:
            return
        if guild.auth is False:
            return
        password = random.randint(
            1000,
            9999
            )
        image = ImageCaptcha()
        data = image.generate(password)
        Auth.create(
            id=member.id,
            password=password
            )
        file = discord.File(
            data,
            filename="pass.png"
            )
        channel = self.get_channel(guild.authch)
        await channel.send(
            f"{member.mention}画像にある数字を入力してください。",
            file=file
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        auth = Auth(
            message.author.id
            ).get()
        guild = Guild(
            message.guild.id
            ).get()
        if guild.auth is False:
            return

        if auth:
            if guild.authch == message.channel.id:
                if auth.password == message.content:
                    await message.channel.reply(
                        "認証に成功しました。"
                        )
                    role = self.get_role(
                        guild.authrole
                        )
                    await message.author.add_roles(
                        role=role,
                        reason="認証のため。"
                        )
                else:
                    return await message.channel.send(
                        "パスワードが違います。"
                        )
            else:
                return

        else:
            return

    @commands.command()
    async def authtest(self, ctx):
        guild = Guild(ctx.author.guild.id).get()
        if guild.auth is False:
            return
        image = ImageCaptcha()
        password = random.randint(
            1000,
            9999
            )
        data = image.generate(
            password
            )
        image.write(password,
                    'out.png'
                    )
        Auth.create(
            id=ctx.author.id,
            password=password
            )
        file = discord.File(
            "GBot/cogs/I/Image/out.png",
            filename="pass.png"
            )
        channel = guild.auth_ch
        await channel.send(
            f"{ctx.author.mention}画像にある数字を入力してください。",
            file=file
            )


def setup(bot):
    return bot.add_cog(
        Authsys(bot)
        )
