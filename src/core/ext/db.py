import config
from core.ext import Logger
from pymongo import MongoClient


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.load_data()
        return cls._instance

    def load_data(self):
        """Initialize MongoDB connections and configuration data"""
        if hasattr(self, 'maindb'):  # Check if already loaded
            return
        try:
            # Primary MongoDB client and collections
            Logger.info("Database Connecting...")
            self.client = MongoClient(config.MONGO_URI)
            self.db = self.client[config.DB_NAME]
            self.greets = self.db["greets"]
            self.autoroles = self.db["autoroles"]

            
            Logger.info("Database Connected.")
   
        except Exception as e:
            Logger.warning(f"Error loading database or configuration data: {e}")

