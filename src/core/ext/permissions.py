from discord.ext import commands
from discord import app_commands



from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.bot import Gameonix


def maintenance_notice(message: str = "This command is currently under maintenance. Please check back later."):
    async def predicate(ctx:commands.Context):
        await ctx.send(str(message), ephemeral=True)
        return True
    return commands.check(predicate)