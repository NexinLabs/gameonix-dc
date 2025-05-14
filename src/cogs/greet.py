from discord import Embed, TextChannel, Member, Guild, app_commands
from discord.ext import commands
from core.ext.models import GreetModel
from traceback import format_exc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.bot import Gameonix


class GreetMember:
    def __init__(self, member:Member) -> None:
        self.name = member.name
        self.id = member.id
        self.mention = member.mention
        self.display_name = member.display_name
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


async def send_greet_message(bot:"Gameonix", member:Member, channel_id:int=None) -> None:
        _greet_objs = GreetModel.get_greet_by_guild(member.guild.id)
        if not _greet_objs: 
            return

        for _greet_obj in _greet_objs:
            channel = bot.get_channel(_greet_obj.channel_id)

            if not channel or not isinstance(channel, TextChannel):
                continue

            if not channel.permissions_for(member.guild.me).send_messages:
                continue

            if _greet_obj.is_embed:
                embed = Embed(
                    color=bot.color.random(),
                    description=_greet_obj.greet_msg.format(member=GreetMember(member), guild=GreetGuild(member.guild))
                )


                if (member.guild.icon is not None) and _greet_obj.is_thumbnail:
                    
                    embed.set_thumbnail(url=member.guild.icon.url)

                if _greet_obj.image_url and _greet_obj.is_image:
                    embed.set_image(url=_greet_obj.image_url)

                await channel.send(
                    embed=embed,
                    content=_greet_obj.content.format(member=member, guild=GreetGuild(member.guild))
                )

                # Check if the channel is the same as the greeting channel
                if channel_id == _greet_obj.channel_id:
                    break

                continue

            await channel.send(
                content=_greet_obj.content.format(member=GreetMember(member), guild=member.guild) + _greet_obj.greet_msg)


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
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    @commands.has_permissions(manage_guild=True)
    async def test(self, ctx:commands.Context, channel:TextChannel) -> None:
        if ctx.author.bot:
            return
        
        await send_greet_message(self.bot, ctx.author, channel.id)
        await ctx.send("Greeting message sent.")

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


    @greet.group(name="toggle", description="Toggle greet configs")
    @commands.guild_only()
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def toggle(self, ctx:commands.Context) -> None:
        if ctx.invoked_subcommand:
            return
        
        await ctx.send_help(ctx.command)



    @toggle.command(name="embed", description="Toggle embed greeting")
    @app_commands.describe(channel="The channel to toggle the embed greeting")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def toggle_embed(self, ctx:commands.Context, channel:TextChannel) -> None:
        if ctx.author.bot:
            return
        try:
            _greeting = GreetModel.get_greet(channel.id)
            if not _greeting:
                return await ctx.send("No greeting message found for this channel.")

            _greeting.is_embed = not _greeting.is_embed
            _greeting.save()
            await ctx.send(f"Embed greeting toggled to {'enabled' if _greeting.is_embed else 'disabled'}.")
        except Exception as e:
            print(format_exc())
            await ctx.send(f"Error toggling embed greeting: {e}")


    @toggle.command(name="image", description="Toggle image greeting")
    @app_commands.describe(channel="The channel to toggle the image greeting")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def toggle_image(self, ctx:commands.Context, channel:TextChannel) -> None:
        if ctx.author.bot:
            return
        try:
            _greeting = GreetModel.get_greet(channel.id)
            if not _greeting:
                return await ctx.send("No greeting message found for this channel.")

            _greeting.is_image = not _greeting.is_image
            _greeting.save()

            await ctx.send(f"Image greeting `{'enabled' if _greeting.is_image else 'disabled'}`")
        except Exception as e:
            await ctx.send(f"Error toggling image greeting: {e}")


    @toggle.command(name="thumbnail", description="Toggle thumbnail greeting")
    @app_commands.describe(channel="The channel to toggle the thumbnail greeting")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def toggle_thumbnail(self, ctx:commands.Context, channel:TextChannel) -> None:
        if ctx.author.bot:
            return
        try:
            _greeting = GreetModel.get_greet(channel.id)
            if not _greeting:
                return await ctx.send("No greeting message found for this channel.")

            _greeting.is_thumbnail = not _greeting.is_thumbnail
            _greeting.save()

            await ctx.send(f"Thumbnail greeting `{'enabled' if _greeting.is_thumbnail else 'disabled'}`")
        except Exception as e:
            await ctx.send(f"Error toggling thumbnail greeting: {e}")








    @greet.group(name="set", description="Set the greeting message")
    async def set(self, ctx:commands.Context) -> None:
        if ctx.invoked_subcommand:
            return
        await ctx.send_help(ctx.command)



    @set.command(name="message", description="Set the greeting message")
    @app_commands.describe(channel="The channel to set the greeting message", message="Greeting message")
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
    @app_commands.describe(
        previous_channel="The previous channel to set the greeting message", 
        new_channel="The new channel to set the greeting message")
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
    @app_commands.describe(
        channel="The channel to set the greeting image",
        image_url="https://xyz.c/image.png")
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
            _greeting = GreetModel.get_greet(channel.id)
            if not _greeting:
                return await ctx.send("No greeting message found for this channel.")

            _greeting.image_url = image_url
            _greeting.is_image = True
            _greeting.save()
            await ctx.send("Greeting image set successfully.")

        except Exception as e:
            await ctx.send(f"Error setting greeting image: {e}")



    @set.command(name="content", description="Set the greeting content")
    @app_commands.describe(channel="The channel to set the greeting content", content="Greeting content")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.cooldown(2, 60, commands.BucketType.user)
    @commands.bot_has_permissions(send_messages=True, embed_links=True, manage_messages=True)
    async def set_content(self, ctx: commands.Context, channel:TextChannel, *, content:str) -> None:
        if ctx.author.bot:
            return
        if len(content) > 200:
            return await ctx.send("Content is too long. Please keep it under 200 characters.")

        try:
            _greeting = GreetModel.get_greet(channel.id)
            if not _greeting:
                return await ctx.send("No greeting message found for this channel.")

            _greeting.content = content
            _greeting.save()
            await ctx.send("Greeting content set successfully.")

        except Exception as e:
            await ctx.send(f"Error setting greeting content: {e}")



    @greet.command(name="config", description="Show the list of greeting channels")
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
    @app_commands.describe(channel="The channel to remove the greeting message")
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
        if member.bot: 
            return

        _greet_objs = GreetModel.get_greet_by_guild(member.guild.id)
        if not _greet_objs: 
            return

        for _greet_obj in _greet_objs:
            channel = self.bot.get_channel(_greet_obj.channel_id)

            if not channel or not isinstance(channel, TextChannel):
                continue

            if not channel.permissions_for(member.guild.me).send_messages:
                continue

            if _greet_obj.is_embed:
                embed = Embed(
                    color=self.bot.color.random(), 
                    description=_greet_obj.greet_msg.format(member=GreetMember(member), guild=GreetGuild(member.guild))
                )

                if _greet_obj.is_thumbnail and member.guild.icon:
                    embed.set_thumbnail(url=member.guild.icon.url)

                if _greet_obj.image_url and _greet_obj.is_image:
                    embed.set_image(url=_greet_obj.image_url)

                await channel.send(
                    embed=embed,
                    content=_greet_obj.content.format(member=member, guild=GreetGuild(member.guild))
                )
                continue

            await channel.send(
                content=_greet_obj.content.format(member=GreetMember(member), guild=member.guild) + _greet_obj.greet_msg)

