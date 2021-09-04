import random

import discord
from captcha.image import ImageCaptcha
from discord.ext import commands
from core.bot import GBot
from models.auth import Auth
from models.guild import Guild
import captcha

class auth(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot
        self.image = ImageCaptcha()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        auth = await Auth.create(member.id)
        code = random.randint(1000,9999)
        await auth.set(code=code)
        image = self.ImageCaptcha()
        data = image.generate(code)
        image.write(code, 'out.png')
        file = discord.File("cogs/Images/out.png", filename="auth.png")
        guild = await Guild(member.guild.id).get()
        channel = self.bot.get_channel(guild.auth_ch)
        await channel.send(f"{member.mention}画像に表示されている数字を入力してください。", file=file)

    @commands.Cog.listener()
    async def on_message(self, message):
        auth = await Auth(message.author.id).get()
        guild = await Guild(message.guild.id)
        if auth:
            if message.content == auth.code:
                role = self.bot.get_role(guild.auth_role)
                await message.channel.send("認証に成功しました。")
                await message.author.add_role(role)
            else:   
                return
        
        else:
            return
def setup(bot):
    return bot.add_cog(auth(bot))
