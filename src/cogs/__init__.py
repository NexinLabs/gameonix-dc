from typing import TYPE_CHECKING
from cogs.tickets import Ticket
from cogs.test import Test
from cogs.greet import Greeting
from cogs.dev import DevOnlyCog
from cogs.utility import UtilityCog


if TYPE_CHECKING:
    from core.bot import Gameonix


async def setup(bot: "Gameonix") -> None:
    await bot.add_cog(Test(bot))
    await bot.add_cog(Greeting(bot))
    await bot.add_cog(Ticket(bot))
    await bot.add_cog(DevOnlyCog(bot))
    await bot.add_cog(UtilityCog(bot))