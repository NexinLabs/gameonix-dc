import os
from dotenv import load_dotenv
load_dotenv()


SHARD_COUNT = 1
COMMAND_PREFIX = "-"
BOT_TOKEN= os.getenv("BOT_TOKEN", "")
GREET_MESSAGE = ""
TESTING_SERVERS = [
    937038620756426832,
    1298526943775424574
]