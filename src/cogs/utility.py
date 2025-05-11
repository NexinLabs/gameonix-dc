import os
import psutil
from discord import Embed
from discord.ext import commands
from core.ext import emoji, color
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from core.bot import Gameonix




class UtilityCog(commands.Cog):
    def __init__(self, bot: "Gameonix") -> None:
        self.bot = bot

    @commands.hybrid_command(name="botinfo", with_app_command = True, aliases=["bi","info"], description="Get the bot's information.")
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True)
    async def botinfo(self, ctx:commands.Context):
        if ctx.author.bot:
            return
        await ctx.defer(ephemeral=True)
        memory = psutil.virtual_memory()
        mem_percent = f"{(psutil.Process(os.getpid()).memory_percent()):.2f}"
        system_info = f"`{memory.total / (1024**3):.2f} GB`/ `{psutil.Process(os.getpid()).memory_info().rss//2**20} MB`/ `{mem_percent}%`"
        emb = Embed(title=ctx.guild.me.name, color=color.GREEN)
        emb.add_field(name=f"{emoji.ONLINE} __Latency__", value=f"`{round(self.bot.latency*1000)}ms`", inline=True)
        emb.add_field(name=f"{emoji.RAM} __Memory(Total/Usage/Percent)__", value=f"{system_info}", inline=False)
        return await ctx.send(embed=emb)