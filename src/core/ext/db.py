import sqlite3

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

def initialize_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS greets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            greet_msg TEXT,
            channel_id INTEGER UNIQUE,
            guild_id INTEGER,
            image_url TEXT
        )''')
    connection.commit()

def remove_greet(guild_id:int, channel_id:int):
    cursor.execute('''
        DELETE FROM greets WHERE guild_id = ? AND channel_id = ?
    ''', (guild_id, channel_id))
    connection.commit()

def add_greet(guild_id : int, channel_id: int, greet_msg:str, image_url:str):
    try:
        cursor.execute('''
            INSERT INTO greets(greet_msg, channel_id, guild_id, image_url)
            VALUES (?, ?, ?, ?)
        ''', (greet_msg, channel_id, guild_id, image_url))
        connection.commit()
        print(f"Added greet message: {greet_msg} to channel: {channel_id} in guild: {guild_id}")
    except sqlite3.IntegrityError:
        print(f"Channel {channel_id} already has a greet message in guild {guild_id}.")

initialize_db()
greet_msg = "Hello, welcome to the server!"
channel_id = 1234567890
guild_id = 9876543210
image_url = "https://example.com/image.png"

add_greet(guild_id, channel_id, greet_msg, image_url)