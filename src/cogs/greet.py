from discord import Embed, TextChannel
from discord.ext import commands
from core.ext.models import GreetModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.bot import Gameonix



class Greeting(commands.Cog):
    def __init__(self, bot:"Gameonix") -> None:
        self.bot = bot
        self.greeting : GreetModel = None


    @commands.hybrid_group(name="greet", description="Greeting commands")
    async def greet(self, ctx:commands.Context) -> None:
        if ctx.invoked_subcommand:
            return
        await ctx.send_help(ctx.command)



    @greet.command(name="test", description="Test the greet command")
    async def test(self, ctx:commands.Context, channel:TextChannel) -> None:
        _greet_obj = GreetModel.get_greet(channel.id)
        if not _greet_obj:
            return await ctx.send("No greeting message found for this channel.")
        
        await ctx.send(
            embed = Embed(color= self.bot.color.RED,description=_greet_obj.greet_msg)
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

