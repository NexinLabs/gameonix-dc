import os
from dotenv import load_dotenv
load_dotenv()


SHARD_COUNT = 1
COMMAND_PREFIX = "-"
BOT_TOKEN= os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
GREET_MESSAGE = ""
DB_NAME = "GameonixDB"
TESTING_SERVERS = [
    937038620756426832,
    1298526943775424574
]