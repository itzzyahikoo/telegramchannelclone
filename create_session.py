from telethon import TelegramClient
from dotenv import load_dotenv
import os

# Load .env from current folder
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME") or "session"

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

import asyncio

async def main():
    await client.start()
    print(f"✅ Session file '{SESSION_NAME}.session' created successfully!")
    me = await client.get_me()
    print(f"Signed in as {me.first_name} (@{me.username})")
    await client.disconnect()

asyncio.run(main())
