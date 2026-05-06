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
    return "Bot is Live and Running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- TELEGRAM BOT DETAILS ---
API_ID = int(os.environ.get("API_ID", 12345))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("my_bypasser", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Bhai, Bot ek dum mast chal raha hai! Link bhejo, main koshish karta hoon.")

@app.on_message(filters.text & ~filters.command("start"))
async def bypass_handler(client, message):
    url = message.text
    status = await message.reply_text("Bypassing... ⏳")
    
    direct_link = None

    # --- METHOD 1: Bypass.vip API ---
    try:
        r1 = requests.get(f"https://api.bypass.vip/bypass?url={url}").json()
        if r1.get("status") == "success":
            direct_link = r1.get("destination")
    except:
        pass

    # --- METHOD 2: Alternative API (Agar pehli fail ho) ---
    if not direct_link:
        try:
            # Ye ek aur public bypasser hai
            r2 = requests.get(f"https://api.discut.net/bypass?url={url}").json()
            direct_link = r2.get("destination") or r2.get("url")
        except:
            pass

    # --- FINAL CHECK ---
    if direct_link and direct_link != "None":
        await status.edit(f"✅ **Bypassed Link:**\n\n`{direct_link}`")
    else:
        await status.edit("❌ **Bhai, ye link bypass nahi ho pa raha.**\n\n**Wajah:**\n1. Shortener bahut strong hai.\n2. API limit khatam ho gayi hai.\n3. Link invalid hai.")

# --- MAIN STARTING FUNCTION ---
async def main():
    threading.Thread(target=run_web, daemon=True).start()
    await app.start()
    print("--- BOT IS ONLINE ---")
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
