import os
import asyncio
import threading
import requests
from flask import Flask
from pyrogram import Client, filters, idle

# --- RENDER PORT BINDING (Flask) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Live!"

def run_web():
    # Render automatically sets the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- TELEGRAM BOT DETAILS ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("my_bypasser", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Bhai, Bot Render par ek dum mast chal raha hai! Link bhejo.")

@app.on_message(filters.text & ~filters.command("start"))
async def bypass_handler(client, message):
    url = message.text
    status = await message.reply_text("Bypassing... ⏳")
    
    try:
        # Public Bypass API
        api_url = f"https://api.bypass.vip/bypass?url={url}"
        r = requests.get(api_url).json()
        
        if r.get("status") == "success":
            direct_link = r.get("destination")
            await status.edit(f"✅ **Bypassed Link:**\n\n{direct_link}")
        else:
            await status.edit("❌ Ye link bypass nahi ho paya. API limit ya unsupported link ho sakta hai.")
            
    except Exception as e:
        await status.edit(f"❌ Error: {str(e)}")

# --- MAIN STARTING FUNCTION ---
async def main():
    # 1. Flask ko background thread mein chalao
    threading.Thread(target=run_web, daemon=True).start()
    
    # 2. Bot ko start karo
    await app.start()
    print("--- BOT STARTED SUCCESSFULLY ---")
    
    # 3. Bot ko chalaaye rakho
    await idle()
    
    # 4. Stop safely
    await app.stop()

if __name__ == "__main__":
    # Event loop setup for Render/Python 3.10+
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
