import psutil
from discord import Embed
from discord.ext import commands


class DevOnlyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command(hidden=True)
    @commands.is_owner()
    async def system(self, ctx:commands.Context):
        if ctx.author.bot:return
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        detail = f"""
Total RAM : {memory.total / (1024**3):.2f} GB\n
CPU Cores : P: {psutil.cpu_count(logical=False)}, L: {psutil.cpu_count(logical=True)}\n
CPU Usage : {cpu_usage}%\n
RAM Usage : {memory.used//10**6} MB({memory.percent}%)\n
Total Disk: {disk.total//10**9} GB\n
Disk Usage: {disk.used//10**9} GB({disk.percent}%)
        """
        await ctx.send(embed=Embed(title="System Information", description=detail, color=0x00ff00))
       