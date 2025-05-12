import cogs
import config
from discord.ext import commands
from core.ext import color, emoji, Logger
from core.ext.db import Database
from core.ext import models
from discord import Activity, ActivityType, AllowedMentions
from discord import Intents, Object, Message


class Gameonix(commands.AutoShardedBot):
        def __init__(self) -> None:
            self.config = config
            self.color = color
            self.emoji = emoji
            self.db = Database()
            self.models = models
            self.logger = Logger

            
            super().__init__(
                shard_count=config.SHARD_COUNT, 
                command_prefix= commands.when_mentioned_or(config.COMMAND_PREFIX),
                intents=Intents.all(),
                allowed_mentions=AllowedMentions(everyone=False, roles=False, replied_user=True, users=True),
                activity=Activity(type=ActivityType.listening, name=f"{config.COMMAND_PREFIX}help")
        )
            
        async def on_ready(self) -> None:
            self.logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
            self.logger.info(f"Shard ID: {self.shard_id}")
            self.logger.info(f"Shard Count: {self.shard_count}")
            self.logger.info(f"Commands : {len(self.tree.get_commands())}")
            await self.change_presence(activity=Activity(type=ActivityType.listening, name="-help"))
        
        async def setup_hook(self) -> None:
            await cogs.setup(self)
            await self.tree.sync()
            for guild in self.config.TESTING_SERVERS:
                await self.tree.sync(guild=Object(id=guild))

        async def on_message(self, message:Message):
             if message.author.bot:
                return
             await self.process_commands(message)
        
