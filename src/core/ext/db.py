import sqlite3

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

def initialize_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS greets (
            channel_id INTEGER PRIMARY KEY,
            guild_id INTEGER,
            greet_msg TEXT,
            image_url TEXT
        )''')
    connection.commit()


initialize_db()