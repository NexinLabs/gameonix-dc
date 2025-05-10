

from discord import Embed, app_commands, Interaction
from discord.ext import commands

from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from core.bot import Gameonix


class Greeting(commands.Cog):
    def __init__(self, bot: "Gameonix") -> None:
        self.bot = bot

    @app_commands.command(name="greet", description="Greet the bot")
    async def greet(self, interaction:Interaction) -> None:
        embed = Embed(
            title="Hello!",
            description="Welcome to the server! I'm here to assist you.",
            color=0x00FF00
        )
        await interaction.response.send_message(embed=embed)
        