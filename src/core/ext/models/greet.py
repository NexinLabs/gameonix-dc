from core.ext.db import Database
import functools

greeting_cache:dict = {}
collection = Database().greets


class GreetModel:
    def __init__(self, kwargs:dict):
        self.channel_id:int = kwargs.get("channel_id")
        self.guild_id:int = kwargs.get("guild_id")
        self.greet_msg:str = kwargs.get("greet_msg")
        self.content:str = kwargs.get("content") or "Hey, {mention}"
        self.image_url:str = kwargs.get("image_url")
        self.is_image:bool = kwargs.get("is_image", False)
        self.is_embed:bool = kwargs.get("is_embed", True)
        self.is_thumbnail:bool = kwargs.get("is_thumbnail", False)


    def to_dict(self) -> dict:
        return {
            "channel_id": self.channel_id,
            "guild_id": self.guild_id,
            "greet_msg": self.greet_msg,
            "content": self.content,
            "image_url": self.image_url,
            "is_embed": self.is_embed,
            "is_thumbnail": self.is_thumbnail,
            "is_image": self.is_image
        }

    def __repr__(self):
        return f"GreetModel(channel_id={self.channel_id}, guild_id={self.guild_id}, greet_msg={self.greet_msg}, content={self.content}, image_url={self.image_url}, is_embed={self.is_embed}, is_thumbnail={self.is_thumbnail}, is_image={self.is_image})"

    def __str__(self):
        return f"GreetModel(channel_id={self.channel_id}, guild_id={self.guild_id}, greet_msg={self.greet_msg}, content={self.content}, image_url={self.image_url}, is_embed={self.is_embed}, is_thumbnail={self.is_thumbnail}, is_image={self.is_image})"


    @staticmethod
    def create(
        channel_id:int, 
        guild_id:int, 
        greet_msg:str, 
        content:str=None, 
        image_url:str=None, 
        is_embed:bool=True, 
        is_thumbnail:bool=False, 
        is_image:bool=False) -> 'GreetModel':

        _greet:dict = collection.find_one({"channel_id": channel_id})
        if _greet:
            return None
        
        new_greet = GreetModel(
            {
                "channel_id": channel_id,
                "guild_id": guild_id,
                "greet_msg": greet_msg,
                "content": content or "Hey, {mention}",
                "image_url": image_url,
                "is_embed": is_embed,
                "is_thumbnail": is_thumbnail,
                "is_image": is_image
            }
        )
        new_greet.save()
        return new_greet


    @staticmethod
    @functools.cache
    def get_greet(channel_id:int)-> 'GreetModel':
        _greet:dict = collection.find_one({"channel_id": channel_id})
        if not _greet:
            return None
        return GreetModel(_greet)
    

    @staticmethod
    def get_greet_by_guild(guild_id:int)-> 'list[GreetModel]':
        _greet:list[dict] = collection.find({"guild_id": guild_id})
        if not _greet:
            return None

        return [GreetModel(g) for g in _greet]


    @staticmethod
    def remove_greet(channel_id:int):
        _greet:dict = collection.find_one({"channel_id": channel_id})
        if not _greet:
            return None
        
        collection.delete_one({"channel_id": channel_id})
        greeting_cache.pop(channel_id, None)
        return True


    def save(self):
        collection.update_one(
            {"channel_id": self.channel_id}, 
            {"$set": self.to_dict()}, 
            upsert=True
        )
        greeting_cache[self.channel_id] = self
        return True
