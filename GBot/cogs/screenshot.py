import discord
from discord.ext import commands
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


class ScreenShot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chrome_driver = "home/tasuren/GBot/chromedriver"

    def get_screenshot(self, ctx: commands.Context, url: str):
        options = Options()
        options.add_argument('--hide-scrollbars')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(self.chrome_driver, options=options)
        driver.set_window_size(1024, 768)
        # 暗黙的に指定時間待つ（秒）
        driver.implicitly_wait(10)
        driver.get()

        try:
            # articleタグを探す
            driver.find_element_by_tag_name("article")
        except NoSuchElementException:
            return 1
        finally:
            driver.save_screenshot('ss.png')
            driver.quit()
            return 0

    @commands.command(name="ss")
    async def screenshot(self, ctx: commands.Context, url):
        get_sc = await self.get_screenshot(ctx, url)
        if get_sc == 0:
            await ctx.send("申し訳ありません。\n問題が発生したため指定のサイトにアクセスできませんでした。")
            return
        file = discord.File("GBot/result.png", filename="ss.png")
        embed = discord.Embed(title="スクリーンショット結果", description=" ")
        embed.set_image(url="attachment::/ss.png")
        await ctx.send(file=file, embed=embed)
