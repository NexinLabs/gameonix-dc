from discord.ext import commands



class Test(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def sync(self, ctx:commands.Context) -> None:
        await self.bot.tree.sync(guild=ctx.guild)

    @commands.hybrid_group(invokewithout_command=True, name="test", description="Test commands")
    async def test(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand:
            return
        await ctx.send_help(ctx.command)

    
    @test.command(name="ping", description="Ping the bot")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send("Pong!")