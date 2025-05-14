from discord.ext import commands
from discord import app_commands, Role
from core.ext import permissions


from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from core.bot import Gameonix



class RoleCog(commands.Cog):
    def __init__(self, bot:'Gameonix') -> None:
        self.bot = bot

    @commands.hybrid_group(name="autorole", description="Auto role management commands", invoke_without_command=True)
    async def autorole(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand:
            return
        await ctx.send_help(ctx.command)

    @autorole.group(name="add", description="Add auto roles to the guild")
    async def autorole_add(self, ctx: commands.Context) -> None:
        if ctx.invoked_subcommand:
            return
        await ctx.send_help(ctx.command)


    @autorole_add.command(name="human", description="Add auto roles to human members")
    @app_commands.describe(role="The role to add")
    @commands.guild_only()
    @app_commands.guild_only()
    @permissions.maintanance_notice() # This is a placeholder for the maintanance notice
    async def autorole_add_human(self, ctx: commands.Context, role: Role) -> None:
        """Add auto roles to human members"""
        guild = ctx.guild

        _autoroles = self.bot.models.GuildAutoRoleModel.findOne(guild.id)
        if not _autoroles:
            _autoroles = self.bot.models.GuildAutoRoleModel.create(
                guild_id=guild.id,
                auto_role_human=role.id
            )
            if not _autoroles:
                return await ctx.send("Failed to create auto role model")
            await ctx.send(f"Added {role.mention} to auto roles for human members")
            return


        if role.id == _autoroles.auto_role_human:
            return await ctx.send(f"{role.mention} is already set as auto role for human members")
        
        _autoroles.auto_role_human=role.id
        _autoroles.save()
        await ctx.send(f"Added {role.mention} to auto roles for human members")



    @autorole_add.command(name="bot", description="Add auto roles to bot members")
    @commands.guild_only()
    @app_commands.guild_only()
    @app_commands.describe(role="The role to add")
    @permissions.maintanance_notice() # This is a placeholder for the maintanance notice
    async def autorole_add_bot(self, ctx: commands.Context, role: Role) -> None:
        """Add auto roles to bot members"""
        guild = ctx.guild

        _autoroles = self.bot.models.GuildAutoRoleModel.findOne(guild.id)
        if role.id == _autoroles.auto_role_bot:
            return await ctx.send(f"{role.mention} is already set as auto role for bot members")
        
        _autoroles.auto_role_bot=role.id
        _autoroles.save()
        await ctx.send(f"Added {role.mention} to auto roles for bot members")

        if not _autoroles:
            _autoroles = self.bot.models.GuildAutoRoleModel.create(
                guild_id=guild.id,
                auto_roles_bot=role.id
            )
            if not _autoroles:
                return await ctx.send("Failed to create auto role model")
            await ctx.send(f"Added {role.mention} to auto roles for bot members")


            