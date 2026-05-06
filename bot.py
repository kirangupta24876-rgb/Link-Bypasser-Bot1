import os
import threading
import requests
from flask import Flask
from pyrogram import Client, filters

# --- RENDER PORT BINDING (Isse Error nahi aayega) ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is Live!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

# --- TELEGRAM BOT LOGIC ---
API_ID = int(os.environ.get("API_ID", 12345)) # Render Variables se lega
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("my_bypasser", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Bhai, Main zinda hoon! Link bhejo bypass karne ke liye.")

@app.on_message(filters.text & ~filters.command("start"))
def bypass_handler(client, message):
    url = message.text
    status = message.reply_text("Bypassing... ⏳")
    
    # Bypass API (Multiple try karega)
    try:
        # API 1
        api_url = f"https://api.bypass.vip/bypass?url={url}"
        r = requests.get(api_url).json()
        
        if r.get("status") == "success":
            direct_link = r.get("destination")
            status.edit(f"✅ **Bypassed Link:**\n\n{direct_link}")
        else:
            status.edit("❌ Bhai, ye link ye API support nahi kar rahi.")
            
    except Exception as e:
        status.edit(f"❌ Error: {str(e)}")

# --- DONO KO EK SAATH CHALANA ---
if __name__ == "__main__":
    # Web server ko alag thread mein start karo
    threading.Thread(target=run_web).start()
    # Bot ko start karo
    print("Bot starting...")
    app.run()
