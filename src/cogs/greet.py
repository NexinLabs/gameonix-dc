from discord import Embed, TextChannel, Member, Guild
from discord.ext import commands
from core.ext.models import GreetModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.bot import Gameonix


class GreetMember:
    def __init__(self, member:Member) -> None:
        self.name = member.name
        self.id = member.id
        self.global_name = member.global_name
        self.avatar_url = member.avatar.url if member.avatar else None
        self.banner_url = member.banner.url if member.banner else None


class GreetGuild:
    def __init__(self, guild:Guild) -> None:
        self.name = guild.name
        self.id = guild.id
        self.icon_url = guild.icon.url if guild.icon else None
        self.banner_url = guild.banner.url if guild.banner else None
        self.member_count = guild.member_count
        self.owner = guild.owner



class Greeting(commands.Cog):
    def __init__(self, bot:"Gameonix") -> None:
        self.bot = bot
        self.greeting : GreetModel = None


    @commands.hybrid_group(name="greet", description="Greeting commands", invoke_without_command=True)
    async def greet(self, ctx:commands.Context) -> None:
        if ctx.invoked_subcommand:
            return
        await ctx.send_help(ctx.command)



    @greet.command(name="test", description="Test the greet command")
    @commands.guild_only()
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    @commands.has_permissions(manage_guild=True)
    async def test(self, ctx:commands.Context, channel:TextChannel) -> None:
        _greet_obj = GreetModel.get_greet(channel.id)
        if not _greet_obj:
            return await ctx.send("No greeting message found for this channel.")
        
        if _greet_obj.is_embed:
            embed = Embed(color=self.bot.color.random(), description=_greet_obj.greet_msg.format(member=ctx.author, guild=ctx.guild))

            if _greet_obj.image_url:
                embed.set_image(url=_greet_obj.image_url)

            return await ctx.send(
                embed=embed,
                content=_greet_obj.content.format(member=ctx.author, guild=ctx.guild)
            )

        await ctx.send(content=_greet_obj.content.format(member=ctx.author, guild=ctx.guild) + _greet_obj.greet_msg, embed=None)



    @greet.command(name="setup", description="Setup the greeting message")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def create(self, ctx:commands.Context, channel:TextChannel) -> None:
        if ctx.author.bot:
            return
        
        _content = "Hey, {member.mention}!"
        _message = f"""

 {self.bot.emoji.A_CONGO} Welcome To {'{guild.name}'} {self.bot.emoji.A_CONGO}
━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.bot.emoji.A_ARROW}│Read Rules in ⁠<#1367884467594723496>
{self.bot.emoji.A_ARROW}│Chat with Server Members in ⁠<#1367884467821346944>
{self.bot.emoji.A_ARROW}│Take Self Roles From <#1367884467594723497>
{self.bot.emoji.A_ARROW}│Talk to Members in ⁠<#1367884467997511774>
━━━━━━━━━━━━━━━━━━━━━━━━━━━
{self.bot.emoji.A_HEART_BEAT_1} Thanks For Joining {self.bot.emoji.A_HEART_BEAT_1}
""" 
        _greeting = GreetModel(
            channel_id=channel.id,
            guild_id=ctx.guild.id,
            greet_msg=_message,
            content=_content,
            is_embed=True
        )
        _greeting.save()
        self.greeting = _greeting
        await ctx.send("Greeting message setup successfully.")
        




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
    async def set_message(self, ctx: commands.Context, channel:TextChannel, *, message:str) -> None:
        if ctx.author.bot:
            return
        if len(message) > 2000:
            return await ctx.send("Message is too long. Please keep it under 2000 characters.")

        self.greeting = GreetModel.get_greet(channel.id)
        if not self.greeting:
            return await ctx.send("No greeting message found for this channel.")

        try:
            self.greeting.greet_msg = message
            self.greeting.save()
            await ctx.send("Greeting message set successfully.")
        except Exception as e:
            await ctx.send(f"Error setting greeting message: {e}")




    @set.command(name="channel", description="Set the greeting channel")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def set_channel(self, ctx: commands.Context, previous_channel:TextChannel, new_channel:TextChannel) -> None:
        if ctx.author.bot:
            return
        if new_channel == ctx.channel:
            return await ctx.send("You cannot set the same channel as the greeting channel.")

        try:
            if not self.greeting: 
                self.greeting = GreetModel.get_greet(previous_channel.id)
                if not self.greeting:
                    return await ctx.send("No greeting message found for this channel.")
                
            self.greeting.channel_id = new_channel.id
            self.greeting.save()

            await ctx.send(f"Greeting channel set to {new_channel.mention}.")
        except Exception as e:
            await ctx.send(f"Error setting greeting channel: {e}")



    @set.command(name="image", description="Set the greeting image")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def set_image(self, ctx: commands.Context, channel:TextChannel, image_url:str) -> None:
        if ctx.author.bot:
            return
        if not image_url.startswith("https://"):
            return await ctx.send("Please provide a valid image URL.")

        try:
            if not self.greeting: 
                self.greeting = GreetModel.get_greet(channel.id)
                if not self.greeting:
                    return await ctx.send("No greeting message found for this channel.")
                
            self.greeting.image_url = image_url
            self.greeting.save()
            
            await ctx.send("Greeting image set successfully.")

        except Exception as e:
            await ctx.send(f"Error setting greeting image: {e}")


    @greet.command(name="config", description="View the greeting configuration")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def config(self, ctx: commands.Context) -> None:
        _greets = GreetModel.get_greet_by_guild(ctx.guild.id)
        if not _greets:
            return await ctx.send(embed = Embed(description=f"{self.bot.emoji.FAILED} | No Greeting Found", color=self.bot.color.RED))
        
        _descriptions = "".join([
            f"**{self.bot.emoji.A_ARROW} | <#{g.channel_id}> - {g.channel_id}**\n" for g in _greets
        ])

        _embed = Embed(title=f"{self.bot.emoji.A_VERIFIED} | Greeting Configuration", description=_descriptions,  color=self.bot.color.random())
        await ctx.send(embed=_embed)
    

    

    @greet.command(name="remove", description="Remove the greeting message")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def remove(self, ctx: commands.Context, channel :TextChannel) -> None:
        if ctx.author.bot:
            return
        try:
            GreetModel.remove_greet(channel.id)
            await ctx.send("Greeting message removed successfully.")
        except Exception as e:
            await ctx.send(f"Error removing greeting message: {e}")



    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member:Member) -> None:
        if member.bot: return

        _greet_objs = GreetModel.get_greet_by_guild(member.guild.id)
        if not _greet_objs: return

        for _greet_obj in _greet_objs:
            channel = self.bot.get_channel(_greet_obj.channel_id)

            if _greet_obj.is_embed:
                embed = Embed(color=self.bot.color.random(), description=_greet_obj.greet_msg.format(member=GreetMember(member), guild=GreetGuild(member.guild)))

                if member.guild.icon:
                    embed.set_thumbnail(url=member.guild.icon.url)

                if _greet_obj.image_url:
                    embed.set_image(url=_greet_obj.image_url)

                await channel.send(
                    embed=embed,
                    content=_greet_obj.content.format(member=member, guild=GreetGuild(member.guild))
                )
                return

            await channel.send(content=_greet_obj.content.format(member=GreetMember(member), guild=member.guild) + _greet_obj.greet_msg, embed=None)

