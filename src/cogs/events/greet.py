

from discord import Embed, app_commands, Interaction, Member, Guild
from discord.ext import commands

from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from core.bot import Gameonix


class Greeting(commands.Cog):
    def __init__(self, bot: "Gameonix") -> None:
        self.bot = bot
        self.greets = "You're the {}th member to join this server!"


    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member:Member) -> None:
        print("Member joined")
        embed = Embed(
            title="Hello!",
            description=f"Thank you for inviting me to your server! Use -help to see my commands.\n{self.greets.format(member.guild.member_count)}",
            color=0x00FF00
        )
        await self.bot.get_channel(950960353553043476).send(embed=embed)

    @app_commands.command(name="greet", description="Greet the bot")
    async def greet(self, interaction:Interaction) -> None:
        embed = Embed(
            title="Hello!",
            description="Welcome to the server! I'm here to assist you.",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)
