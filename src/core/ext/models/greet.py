from core.ext.db import Database
import functools

greeting_cache:dict = {}
collection = Database().greets


class GreetModel:
    def __init__(self, channel_id:int, guild_id:int, greet_msg:str, content:str=None, image_url:str=None, is_embed:bool=True):
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.greet_msg = greet_msg
        self.content = content or "Hey, {mention}"
        self.image_url = image_url
        self.is_embed = is_embed
        

    def __repr__(self):
        return f"GreetModel(channel_id={self.channel_id}, guild_id={self.guild_id}, greet_msg={self.greet_msg}, content={self.content}, image_url={self.image_url}, is_embed={self.is_embed})"
    
    def __str__(self):
        return f"GreetModel(channel_id={self.channel_id}, guild_id={self.guild_id}, greet_msg={self.greet_msg}, content={self.content}, image_url={self.image_url}, is_embed={self.is_embed})"


    @staticmethod
    @functools.cache
    def get_greet(channel_id:int)-> 'GreetModel':
        _greet:dict = collection.find_one({"channel_id": channel_id})
        if not _greet:
            return None
        
        return GreetModel(
            channel_id=_greet["channel_id"],
            guild_id=_greet["guild_id"],
            greet_msg=_greet["greet_msg"],
            content=_greet.get("content"),
            image_url=_greet.get("image_url"),
            is_embed=_greet.get("is_embed", True)
        )
    
    @staticmethod
    def get_greet_by_guild(guild_id:int)-> 'list[GreetModel]':
        _greet:list[dict] = collection.find({"guild_id": guild_id})
        if not _greet:
            return None
        
        return [GreetModel(
            channel_id=g["channel_id"],
            guild_id=g["guild_id"],
            greet_msg=g["greet_msg"],
            content=g.get("content"),
            image_url=g.get("image_url"),
            is_embed=g.get("is_embed", True)
        ) for g in _greet]

    
    @staticmethod
    def remove_greet(channel_id:int):
        _greet:dict = collection.find_one({"channel_id": channel_id})
        if not _greet:
            return None
        
        collection.delete_one({"channel_id": channel_id})
        greeting_cache.pop(channel_id, None)
        return True


    def save(self):
        collection.update_one({"channel_id": self.channel_id}, {
            "$set": {
                "channel_id": self.channel_id,
                "guild_id": self.guild_id,
                "greet_msg": self.greet_msg,
                "content": self.content,
                "image_url": self.image_url,
                "is_embed": self.is_embed
            }
        }, upsert=True)
        greeting_cache[self.channel_id] = self
        return True
