
import enum
import config 
from core.ext import emoji
from core.ext import color
from discord.ext import commands
from discord.ui import View, Button
from discord import Embed, PermissionOverwrite, Role, Emoji, ButtonStyle, Interaction
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


    @commands.hybrid_group(name="ticket", aliases=["t"], with_app_command = True, description="Ticket System")
    async def ticket(self, ctx:commands.Context):
        if ctx.invoked_subcommand:
            return 
        await ctx.send_help(ctx.command)


    @ticket.command(name="setup", description="Setup Ticket System")
    @commands.guild_only()
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True, manage_channels=True, manage_roles=True)
    async def setup_ticket(self, ctx:commands.Context, mod_role:Role=None, button_label:str=None, button_emoji:Emoji=None, button_color:Buttons=None, *, message:str=None):
        if ctx.author.bot:return
        if config.COMMAND_PREFIX in ctx.message.content:
            return await ctx.reply("Use Slash Command to manage other properties!!", delete_after=10)
        await ctx.defer(ephemeral=True)
        ms = await ctx.send("Creating Ticket Category...")
        overwrites = {
            ctx.guild.default_role: PermissionOverwrite(read_messages=False),
            ctx.guild.me: PermissionOverwrite(read_messages=True),
        }
        if mod_role:
            overwrites[mod_role] = PermissionOverwrite(read_messages=True, send_messages=True, manage_messages=True)

        category = await ctx.guild.create_category("Tickets", overwrites=overwrites)
        ticketChannel = await category.create_text_channel("create-ticket")

        await ms.edit(content="Creating Ticket Channel...")
        await ticketChannel.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=False)
        await ms.edit(content="Creating Ticket Message...")
        embed = Embed(title="Create Ticket", description="Click on the button to create a ticket!!", color=color.GREEN)
        if ctx.guild.icon:
            embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon.url)

        if not button_color:
            button_color = ButtonStyle.blurple

        else:button_color = button_color.value
        view = View().add_item(
            Button(
                emoji=button_emoji or "✅", 
                label=button_label or "Create Ticket", 
                style=button_color, 
                custom_id=f"{self.bot.user.id}-ticket"
            )
        )
        await ms.edit(content="Sending Ticket Message...")
        await ticketChannel.send(embed=embed, view=view)
        await ms.edit(content="Ticket System Setup Done")


    @commands.Cog.listener()
    async def on_interaction(self, interaction:Interaction):
        if interaction.user.bot:return
        if "custom_id" not in interaction.data or interaction.message.author.id != self.bot.user.id:
            return
        
        if interaction.data["custom_id"] == f"{self.bot.user.id}-ticket":

            if not interaction.channel.category: 
                return await interaction.response.send_message("**Please move this channel to a category. to create tickets**", delete_after=10)
            
            channel = await interaction.channel.category.create_text_channel(f"ticket-{interaction.user}", reason="Ticket Created")
            await channel.set_permissions(
                interaction.user, 
                read_messages=True, 
                send_messages=True, 
                attach_files=True, 
                embed_links=True, 
                read_message_history=True, 
                add_reactions=True
            )
            embed = Embed(
                title="Ticket Created", 
                description=f"**{emoji.A_ARROW}Thanks for contacting\n{emoji.A_ARROW}Feel free to communicate**", 
                color=color.GREEN
            )
            view = View().add_item(
                Button(label="Close Ticket", style=ButtonStyle.red, custom_id=f"{self.bot.user.id}SPTcancel")
            )
            await channel.send(f"<@{interaction.user.id}>", embed=embed, view=view)
            await interaction.response.send_message(f"**Ticket <#{channel.id}> Created Successfully**", ephemeral=True, delete_after=10)

        if interaction.data["custom_id"] == f"{self.bot.user.id}SPTcancel":
            closeConfirm = Button(label="Confirm", style=ButtonStyle.red)
            closeCancel = Button(label="Cancel", style=ButtonStyle.green)
            view = View()
            view.add_item(closeConfirm); view.add_item(closeCancel)
            await interaction.response.send_message(embed=Embed(description="Are You Sure?", color=color.RED), view=view, delete_after=10)

            async def closeTicket(interaction:Interaction):
                await interaction.response.send_message(embed=Embed(description="Closing Ticket...", color=color.RED), ephemeral=True)
                await interaction.channel.delete(reason="Ticket Closed")

            async def cancelClose(interaction:Interaction):
                await interaction.message.delete()

            closeConfirm.callback = closeTicket
            closeCancel.callback = cancelClose