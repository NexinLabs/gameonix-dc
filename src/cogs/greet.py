from discord import Embed
from discord.ext import commands
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.bot import Gameonix


class Greeting(commands.Cog):
    def __init__(self, bot:"Gameonix") -> None:
        self.bot = bot
        self.greet_message = """
Hey {member.mention}!
WELCOME TO {member.guild.name}!

〢 read rules in - ⁠𐂡・rules
〢 take self roles in - ⁠𐂡・self-roles
〢 chat with other members - ⁠⸙・general-chat

 Thanks For Joining
 """

    @commands.hybrid_group(name="greet", description="Greeting commands")
    async def greet(self, ctx:commands.Context) -> None:
        if ctx.invoked_subcommand:
            return
        await ctx.send_help(ctx.command)

    @greet.command(name="test", description="Test the greet command")
    async def test(self, ctx:commands.Context) -> None:
        await ctx.send(
            embed = Embed(description=self.greet_message.format(member=ctx.author))
        )

