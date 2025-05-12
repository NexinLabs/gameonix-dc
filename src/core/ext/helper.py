import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.converter import (RoleConverter, TextChannelConverter)



async def channel_input(ctx:commands.Context, check=None, timeout=20):
    check = check or (lambda m: m.channel == ctx.channel and m.author == ctx.author)
    try:
        message: discord.Message = await ctx.bot.wait_for("message", check=check, timeout=timeout)

    except asyncio.TimeoutError:
        return await ctx.send("Time Out! Try Again")
    else:
        try:
            await message.delete()
        except:
            pass
        channel = await TextChannelConverter().convert(ctx, message.content)
        return channel