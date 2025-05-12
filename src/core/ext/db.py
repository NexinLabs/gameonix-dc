import sqlite3

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

def initialize_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS greets (
            channel_id INTEGER PRIMARY KEY,
            guild_id INTEGER,
            greet_msg TEXT,
            content TEXT,
            image_url TEXT,
            is_embed BOOLEAN
        )''')
    connection.commit()
    print("Database initialized successfully.")