from datetime import datetime, timedelta
import os
from telethon.sync import TelegramClient
from telethon import functions, types
import time
import sqlite3

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
source_channel_id = int(os.environ.get('SOURCE_CHANNEL_ID'))
destination_channel_id = int(os.environ.get('DESTINATION_CHANNEL_ID'))
database_file = 'userbot_database.db'

# Connect to the database
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create a table for viewed posts if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS viewed_posts (
        id INTEGER PRIMARY KEY,
        message_id INTEGER,
        date INTEGER
    )
''')
conn.commit()

# Connect to Telegram
client = TelegramClient('userbot_session', api_id, api_hash)
client.start()

# Forward new posts from the source channel to the destination channel
async def forward_new_posts():
    async for message in client.iter_messages(source_channel_id):
        if not isinstance(message, types.MessageService):
            # Check if the message has been viewed before
            cursor.execute('SELECT id FROM viewed_posts WHERE message_id = ?', (message.id,))
            result = cursor.fetchone()

            if not result:
                # Forward the new message to the destination channel
                await client.forward_messages(destination_channel_id, message)

                # Insert the viewed post into the database
                cursor.execute('INSERT INTO viewed_posts (message_id, date) VALUES (?, ?)', (message.id, int(datetime.now().timestamp())))
                conn.commit()

# Run the forward_new_posts function periodically
with client:
    while True:
        client.loop.run_until_complete(forward_new_posts())

        # Sleep for one minute before polling again
        next_poll_time = datetime.now() + timedelta(seconds=1)
        time_to_sleep = (next_poll_time - datetime.now()).total_seconds()
        time.sleep(time_to_sleep)
