from typing import TYPE_CHECKING
from cogs.events.greet import Greeting


if TYPE_CHECKING:
    from core.bot import Gameonix


async def setup(bot: "Gameonix") -> None:
    print("Loading events cog...")
    await bot.add_cog(Greeting(bot))