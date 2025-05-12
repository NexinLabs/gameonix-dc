from core.ext.db import connection, cursor
import functools


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
    def get_greet(channel_id:int):
        cursor.execute('''SELECT * FROM greets WHERE channel_id = ?''', (channel_id,))
        result = cursor.fetchone()
        if result:
            return GreetModel(*result)
        return None

    
    @staticmethod
    def remove_greet(channel_id:int):
        cursor.execute('''DELETE FROM greets WHERE channel_id = ?''', (channel_id))
        connection.commit()
        return True


    def save(self):
        if GreetModel.get_greet(self.channel_id):
            cursor.execute('''UPDATE greets SET channel_id = ?, guild_id = ?, greet_msg = ?, content = ?, image_url = ?, is_embed = ? WHERE channel_id = ?''', 
                            (self.channel_id, self.guild_id, self.greet_msg, self.content, self.image_url, self.is_embed, self.channel_id))
            connection.commit()
            return self

        # if no greet exists, create a new one
        cursor.execute('''INSERT INTO greets (channel_id, guild_id, greet_msg, content, image_url, is_embed) VALUES (?, ?, ?, ?, ?, ?)''', 
                        (self.channel_id, self.guild_id, self.greet_msg, self.content, self.image_url, self.is_embed))
        connection.commit()
        return self
