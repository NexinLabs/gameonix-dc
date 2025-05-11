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

    @greet.group(name="set", description="Set the greeting message")
    async def set(self, ctx:commands.Context) -> None:
        if ctx.invoked_subcommand:
            return
        await ctx.send_help(ctx.command)

    @set.command(name="message", description="Set the greeting message")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def set_message(self, ctx: commands.Context, *, message:str) -> None:
        if ctx.author.bot:
            return
        if self.bot.config.COMMAND_PREFIX in ctx.message.content:
            return await ctx.reply("Use Slash Command to manage other properties!!", delete_after=10)
        await ctx.defer(ephemeral=True)
        self.greet_message = message
        await ctx.send("Greeting message set successfully!")
