import os
from dotenv import load_dotenv
load_dotenv()


SHARD_COUNT = 1
COMMAND_PREFIX = "-"
BOT_TOKEN= os.getenv("BOT_TOKEN", "")