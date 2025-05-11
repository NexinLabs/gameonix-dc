from discord.ext import commands
from discord import Activity, ActivityType, AllowedMentions
from discord import Intents
from cogs import events, cmd
import config

class Gameonix(commands.AutoShardedBot):
        def __init__(self) -> None:
            self.config = config

            super().__init__(
                shard_count=config.SHARD_COUNT, 
                command_prefix= commands.when_mentioned_or(config.COMMAND_PREFIX),
                intents=Intents.all(),
                allowed_mentions=AllowedMentions(everyone=False, roles=False, replied_user=True, users=True),
                activity=Activity(type=ActivityType.listening, name="-help")
        )
            
        async def on_ready(self) -> None:
            print(f"Logged in as {self.user} (ID: {self.user.id})")
            print(f"Shard ID: {self.shard_id}")
            print(f"Shard Count: {self.shard_count}")
            print("------")
            await self.change_presence(activity=Activity(type=ActivityType.listening, name="-help"))
        
        async def setup_hook(self) -> None:
            # self.remove_command("help")
            await events.setup(self)
            await cmd.setup(self)
            await self.tree.sync()
        
