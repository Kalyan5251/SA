import psycopg2
import sys
import logging
from app import DATABASE_URL, TELEGRAM_API_URL
import requests

logging.basicConfig(level=logging.INFO)

print("Checking Telegram...")
try:
    res = requests.get(f"{TELEGRAM_API_URL}/getMe")
    print("Telegram getMe status:", res.status_code)
    print("Telegram response:", res.json())
except Exception as e:
    print("Telegram Error:", e)

print("\nChecking Supabase...")
try:
    print(f"Connecting to {DATABASE_URL}")
    conn = psycopg2.connect(DATABASE_URL, connect_timeout=5, sslmode='require')
    print("Supabase connected successfully!")
    conn.close()
except Exception as e:
    print("Supabase connection failed:", e)

print("\nChecking Chatbot instance...")
try:
    from app import bot
    res = bot.process_message("test_user_1", "hi")
    print("Bot responded successfully:", len(res) > 0)
except Exception as e:
    print("Bot test failed:", e)

sys.stdout.flush()
