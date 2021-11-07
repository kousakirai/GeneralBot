import discord
from discord.ext import commands
prefix = "g!"


class Help(commands.DefaultHelpCommand):

    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"

    def get_ending_note(self):
        return (f"各コマンドの説明: {prefix}help <コマンド名>\n"
                f"各カテゴリの説明: {prefix}help <カテゴリ名>\n")

    def command_not_found(self, string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self, command, string):
        instance = isinstance(
            command,
            commands.Group
            ) and len(
                command.all_commands
                )

        if instance > 0:
            # もし、そのコマンドにサブコマンドが存在しているなら
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"

    async def send_bot_help(self, mapping):
        content = ""
        for cog in mapping:
            # 各コグのコマンド一覧を content に追加していく
            command_list = await self.filter_commands(mapping[cog])
            if not command_list:
                # 表示できるコマンドがないので、他のコグの処理に移る
                continue
            if cog is None:
                # コグが未設定のコマンドなので、no_category属性を参照する
                content += f"```\n{self.no_category}```"
            else:
                description = "cog.description"
                content += f"```\n{cog.qualified_name} / {description}\n```"
            for command in command_list:
                content += f"`{command.name}` / {command.description}\n"
            content += "\n"
        embed = discord.Embed(
            title="コマンドリスト",
            description=content, color=0x00ff00
            )

        embed.set_footer(
            text=f"コマンドのヘルプ {self.context.prefix}help コマンド名"
            )

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        content = ""
        command_list = await self.filter_commands(cog.get_commands())

        content += f"```\n{cog.qualified_name} / {cog.description}\n```"
        for command in command_list:
            content += f"`{command.name}` / {command.description}\n"
        content += "\n"
        if not content:
            content = "表示できるコマンドがありません。"

        embed = discord.Embed(
            title="コマンドリスト", description=content, color=0x00ff00)
        embed.set_footer(text=f"コマンドのヘルプ {self.context.prefix}help コマンド名")
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=self.get_command_signature(
            group), description=group.description, color=0x00ff00)
        if group.help:
            embed.add_field(
                name="ヘルプテキスト：",
                value=group.help, inline=False
                )

        content = ""
        command_list = await self.filter_commands(group.commands)
        for command in command_list:
            content += f"`{command.name}` / {command.description}\n"
        embed.add_field(
            name="サブコマンドリスト",
            value=content, inline=False
            )

        embed.set_footer(
            text=f"コマンドのヘルプ {self.context.prefix}help コマンド名"
            )

        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(
            title=self.get_command_signature(command),
            description=command.description, color=0x00ff00
            )
        if command.help:
            embed.add_field(
                name="ヘルプテキスト：",
                value=command.help,
                inline=False
                )
        embed.set_footer(
            text=f"コマンドのヘルプ {self.context.prefix}help コマンド名"
            )
        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(
            title="ヘルプ表示のエラー", description=error,
            color=0xff0000
            )

        await self.get_destination().send(embed=embed)
