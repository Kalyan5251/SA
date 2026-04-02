import os
import requests
import logging
import psycopg2
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask App
app = Flask(__name__)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "8609250788:AAE6sXAdXmDBqOJjULaJOKidbWTIRePpTAg"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

# WhatsApp API Configuration
WHATSAPP_VERIFY_TOKEN = "12345"
WHATSAPP_PHONE_NUMBER_ID = "1131007703421718"
WHATSAPP_ACCESS_TOKEN = "EAAcVulpieqYBRKFC6duBM2ZCZAbObUrgyvSUvOxdP0LRZCSrsSqOqcJkntpu0JTpQjm33lqp5N482rdc9mvldL5sbAxl9ZAI9xzgZBNRXtGZC5sdeovKhrXcYz7CsgPnz5KVnfb9QcPJoC7N56zjTxiyxvtOYncMr5wR7dNSuKITtqrhkZBFC39BNlrtgiq3wqfPJFb9bfJ29d5WKrG7ZB6fuPVO7uJz822kS1iWio9PmLGPIRx1Mt9SWBNbDsKfdYBHtttiNN0Mi6xyyUMIZBg71MAZDZD"
WHATSAPP_API_URL = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"

# Database URL from environment (fallback to hardcoded if not found)
raw_db_url = os.environ.get("DATABASE_URL", "postgresql://postgres.hrbndnvadhqfyncbryxw:Zz9oaKB2z5jUUPpC@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres")
DATABASE_URL = raw_db_url.replace("?pgbouncer=true", "").replace("\n", "").strip()


# Import chatbot engine
try:
    from chatbot_engine import process_message
except ImportError:
    from chatbot_engine import SamriddhiChatbot
    bot = SamriddhiChatbot()
    process_message = bot.process_message

WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", WHATSAPP_ACCESS_TOKEN)

def send_telegram_message(chat_id, text):
    """Helper function to send a message back to Telegram."""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Telegram Message sent to chat_id {chat_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Telegram message to chat_id {chat_id}: {e}")

def send_whatsapp_message(phone_number_id, to, text):
    """Helper function to send a message back via WhatsApp Cloud API."""
    if not WHATSAPP_TOKEN:
        logger.warning("WHATSAPP_TOKEN is not set. Unable to send WhatsApp message.")
        return
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"WhatsApp Message sent to {to}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send WhatsApp message to {to}: {e}")

def save_to_db(chat_id, text, bot_response, platform):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Insert user if they don't exist
        cur.execute("""
            INSERT INTO users (phone, platform) 
            VALUES (%s, %s)
            ON CONFLICT (phone) DO NOTHING;
        """, (str(chat_id), platform))
        
        # Insert the message
        cur.execute("""
            INSERT INTO messages (phone, message, response, platform) 
            VALUES (%s, %s, %s, %s);
        """, (str(chat_id), text, bot_response, platform))
        
        conn.commit()
        print(f"Data saved for {platform}")
    except psycopg2.Error as db_err:
        print(f"Database error: {db_err}")
        if 'conn' in locals() and conn:
            conn.rollback()
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()

def process_telegram_update(update):
    if "message" not in update:
        logger.info("Received Telegram update without a message object. Ignoring.")
        return jsonify({"status": "ok"}), 200
        
    message_data = update.get("message", {})
    chat_id = message_data.get("chat", {}).get("id")
    text = message_data.get("text")

    if not chat_id or not text:
        logger.info("Telegram Message missing chat_id or text. Ignoring.")
        return jsonify({"status": "ok"}), 200

    logger.info(f"Received Telegram message from chat_id {chat_id}: {text}")

    try:
        bot_response = process_message(str(chat_id), text)
        if bot_response:
            send_telegram_message(chat_id, bot_response)
            save_to_db(chat_id, text, bot_response, "Telegram")
    except Exception as e:
        logger.error(f"Error processing Telegram message for {chat_id}: {e}", exc_info=True)

    return jsonify({"status": "ok"}), 200

def process_whatsapp_update(update):
    try:
        for entry in update.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" in value:
                    phone_number_id = value.get("metadata", {}).get("phone_number_id")
                    for message in value.get("messages", []):
                        if message.get("type") == "text":
                            sender_phone = message.get("from")
                            text = message.get("text", {}).get("body")
                            logger.info(f"Received WhatsApp message from {sender_phone}: {text}")
                            
                            bot_response = process_message(str(sender_phone), text)
                            
                            if bot_response:
                                send_whatsapp_message(phone_number_id, sender_phone, bot_response)
                                save_to_db(sender_phone, text, bot_response, "WhatsApp")
    except Exception as e:
        logger.error(f"Error processing WhatsApp message: {e}", exc_info=True)
    
    return jsonify({"status": "ok"}), 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Endpoint to receive updates from Telegram and WhatsApp."""
    if request.method == 'GET':
        # WhatsApp Webhook Verification
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
            logger.info("WhatsApp webhook verified successfully!")
            return challenge, 200
        elif mode or token:
            return "Verification failed", 403
        return "Webhook is active", 200

    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    update = request.get_json()
    
    if update.get("object") == "whatsapp_business_account":
        return process_whatsapp_update(update)
    else:
        return process_telegram_update(update)

@app.route('/', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return "Flask is running and ready to accept webhooks.", 200

if __name__ == '__main__':
    # Run server on port 5000
    app.run(host='0.0.0.0', port=5000)
