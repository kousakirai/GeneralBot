import discord
from discord.ext import commands
import youtube_dl
import asyncio
from GBot.core.bot import GBot

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        dload = not stream
        loop = loop or asyncio.get_event_loop()
        def lam(): return ytdl.extract_info(
            url,
            download=dload
            )
        data = await loop.run_in_executor(
            None,
            lam
            )

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        fname = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(
            discord.FFmpegPCMAudio(
                fname,**ffmpeg_options
                ),
            data=data
            )


class Voicemusic(commands.Cog):
    def __init__(self, bot: GBot):
        self.bot = bot

    @commands.group()
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "引数・コマンドが不正です。"
                )

    @music.command()
    async def play(self, ctx):
        member = ctx.author
        connect = member.voice.channel.connect
        if isinstance(
            connect,
            discord.stageinstance
            ):
            return


def setup(bot):
    return bot.add_cog(
        Voicemusic(
            bot
            )
        )
