
import enum
import config 
from core.ext import color
from discord.ext import commands
from discord.ui import View, Button
from discord import Embed, PermissionOverwrite, Role, Emoji, ButtonStyle
from typing import TYPE_CHECKING
   
if TYPE_CHECKING:
    from core.bot import Gameonix


class Buttons(enum.Enum):
    green = ButtonStyle.green
    red = ButtonStyle.red
    grey = ButtonStyle.grey
    blurple = ButtonStyle.blurple


class Ticket(commands.Cog):
    def __init__(self, bot:"Gameonix") -> None:
        self.bot = bot

    @commands.hybrid_command(name="ticket", with_app_command = True)
    @commands.guild_only()
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True, manage_channels=True, manage_roles=True)
    async def ticket(self, ctx:commands.Context):
        if ctx.author.bot:return
        if config.COMMAND_PREFIX in ctx.message.content:return await ctx.reply("Use Slash Command to manage other properties!!", delete_after=10)
        await ctx.defer(ephemeral=True)
        embed = Embed(title="Ticket System", description="Setup a ticket system for your server.", color=color.GREEN)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(with_app_command = True)
    @commands.guild_only()
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True, manage_channels=True, manage_roles=True)
    async def setup_ticket(self, ctx:commands.Context, mod_role:Role=None, button_label:str=None, button_emoji:Emoji=None, button_color:Buttons=None, *, message:str=None):
        if ctx.author.bot:return
        if config.COMMAND_PREFIX in ctx.message.content:return await ctx.reply("Use Slash Command to manage other properties!!", delete_after=10)
        await ctx.defer(ephemeral=True)
        ms = await ctx.send("Creating Ticket Category...")
        overwrites = {
            ctx.guild.default_role: PermissionOverwrite(read_messages=False),
            ctx.guild.me: PermissionOverwrite(read_messages=True),
        }
        if mod_role:overwrites[mod_role] = PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)
        category = await ctx.guild.create_category("Tickets", overwrites=overwrites)
        ticketChannel = await category.create_text_channel("create-ticket")
        await ms.edit(content="Creating Ticket Channel...")
        await ticketChannel.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=False)
        await ms.edit(content="Creating Ticket Message...")
        embed = Embed(title="Create Ticket", description="Click on the button to create a ticket!!", color=color.GREEN)
        embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)
        if not button_color:button_color = ButtonStyle.blurple
        else:button_color = button_color.value
        view = View().add_item(Button(emoji=button_emoji or "✅", label=button_label or "Create Ticket", style=button_color, custom_id=f"{self.bot.user.id}-ticket"))
        await ms.edit(content="Sending Ticket Message...")
        await ticketChannel.send(embed=embed, view=view)
        await ms.edit(content="Ticket System Setup Done")