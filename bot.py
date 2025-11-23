from dotenv import load_dotenv
import os

# Force load .env from the correct folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)
import asyncio
from telethon import TelegramClient, events
from telethon.errors import ChannelInvalidError, UsernameInvalidError, PeerIdInvalidError

# ============================
# ENVIRONMENT VARIABLES
# ============================
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
SOURCE_USERNAME = os.getenv("SOURCE_USERNAME")   # example: mysourcechannel
TARGET_USERNAME = os.getenv("TARGET_USERNAME")   # example: mybackupchannel
BOT_ADMIN = os.getenv("BOT_ADMIN")               # your Telegram username without @

# ============================
# TELETHON CLIENT
# ============================
client = TelegramClient(SESSION, API_ID, API_HASH)

# ============================
# HELPER: Get entity by username
# ============================
async def get_entity_safe(username):
    try:
        entity = await client.get_entity(username)
        return entity
    except (ChannelInvalidError, UsernameInvalidError, PeerIdInvalidError):
        print(f"[ERROR] Cannot find or access: @{username}")
        return None

# ============================
# STARTUP
# ============================
@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    if event.sender.username != BOT_ADMIN:
        return

    await event.reply(
        "**Bot is running successfully!**\n"
        "Cloning from:\n"
        f"📥 @{SOURCE_USERNAME}\n"
        f"➡️ @{TARGET_USERNAME}"
    )

# ============================
# MESSAGE CLONING HANDLER
# ============================
@client.on(events.NewMessage())
async def clone(event):

    # Only copy from source channel
    if event.chat is None:
        return

    if event.chat.username != SOURCE_USERNAME:
        return

    target = await get_entity_safe(TARGET_USERNAME)
    if not target:
        print("❌ Could not load target channel.")
        return

    try:
        if event.media:
            await client.send_file(
                target,
                event.media,
                caption=event.text or ""
            )
        else:
            await client.send_message(
                target,
                event.text
            )

        print(f"[CLONED] Message forwarded: {event.id}")

    except Exception as e:
        print(f"[ERROR] Failed to clone message: {e}")

# ============================
# RUN BOT
# ============================
async def main():
    print("🚀 Starting bot...")
    await client.start()
    print("✓ Bot Started. Listening for messages...")

    # Check entities on startup
    src = await get_entity_safe(SOURCE_USERNAME)
    tgt = await get_entity_safe(TARGET_USERNAME)

    if not src:
        print(f"❌ SOURCE_CHANNEL @{SOURCE_USERNAME} not found!")
    else:
        print(f"📥 Source OK: @{SOURCE_USERNAME}")

    if not tgt:
        print(f"❌ TARGET_CHANNEL @{TARGET_USERNAME} not found!")
    else:
        print(f"➡️ Target OK: @{TARGET_USERNAME}")

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
