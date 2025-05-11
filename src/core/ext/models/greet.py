from core.ext.db import connection, cursor
from sqlite3 import IntegrityError

class GreetModel:
    def __init__(self, channel_id:int, guild_id:int, greet_msg:str, image_url:str):
        self.channel_id = channel_id
        self.guild_id = guild_id
        self.greet_msg = greet_msg
        self.image_url = image_url

    def __repr__(self):
        return f"Greet(channel_id={self.channel_id}, guild_id={self.guild_id}, greet_msg={self.greet_msg}, image_url={self.image_url})"
    
    
    @staticmethod
    def get_greet(channel_id:int):
        cursor.execute('''SELECT * FROM greets WHERE channel_id = ?''', (channel_id,))
        result = cursor.fetchone()
        if result:
            return GreetModel(*result)
        return None

    
    @staticmethod
    def remove_greet(channel_id:int):
        try:
            cursor.execute('''DELETE FROM greets WHERE channel_id = ?''', (channel_id))
            connection.commit()
            return True
        
        except Exception as e:
            print(f"Error removing greet message from channel {channel_id}: {e}")
            return False


    @staticmethod
    def add_greet(guild_id : int, channel_id: int, greet_msg:str, image_url:str):
        try:
            cursor.execute('''
                INSERT INTO greets(greet_msg, channel_id, guild_id, image_url)
                VALUES (?, ?, ?, ?)
            ''', (greet_msg, channel_id, guild_id, image_url))
            connection.commit()
            return True
        
        except IntegrityError:
            print(f"Channel {channel_id} already has a greet message in guild {guild_id}.")
            return False


