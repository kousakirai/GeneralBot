from discord.ext import commands
import discord
from GBot.models.GBan import Gban


class Gban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def list_add(self, ctx, user: discord.user, reason):
        gban = Gban(user.id).get()
        embed = discord.Embed(title="Gban管理システム", description=" ")
        if gban:
            embed.add_field(name="すでに登録済みです。", value="別のユーザーを指定してください。")
        else:
            reason = f"[Gban執行]{user.name}理由：{reason}"
            Gban.create(id=user.id, reason=reason)
            embed.add_field(name="登録しました。", value="運営が承認するまでしばらくお待ち下さい。")
        return await ctx.send(embed=embed)

    async def list_del(self, ctx, user: discord.user):
        gban = Gban(user.id).get()
        embed = discord.Embed(title="Gban管理システム", description=" ")
        if gban:
            Gban(user.id).delete()
            embed.add_field(name="承認リストから削除しました。", value="再申請する場合は申請し直してください。")
        else:
            embed.add_field(name="登録されていません。", value="申請はg!gban addからできます。")
        return ctx.send(embed=embed)

    @commands.group()
    async def gban(self, ctx):
        if ctx.invoked_subcommand is None:
            return

    @gban.command()
    async def add(self, ctx, Member:discord.Member, reason):
        await self.list_add(ctx, Member, reason)

    @commands.is_owner()
    @gban.command()
    async def delete(self, ctx, member: discord.Member):
        await self.list_del(ctx, member)

    @commands.is_owner()
    @gban.command()
    async def view(self, ctx):
        embed = discord.Embed(title="Gban管理システム", description=" ")
        for user in Gban.all():
            us = self.bot.fetch_user(user.id)
            embed.add_field(name=f"対象者{us.name}", value=f"理由：{user.reason}")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @gban.command()
    async def run(self, ctx):
        pass
def setup(bot):
    return bot.add_cog(Gban(bot))