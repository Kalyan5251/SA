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

# Database URL from environment (fallback to hardcoded if not found)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres.hrbndnvadhqfyncbryxw:Zz9oaKB2z5jUUPpC@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres")


# Import chatbot engine
try:
    from chatbot_engine import process_message
except ImportError:
    from chatbot_engine import SamriddhiChatbot
    bot = SamriddhiChatbot()
    process_message = bot.process_message

def send_message(chat_id, text):
    """Helper function to send a message back to Telegram."""
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Message sent to chat_id {chat_id}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message to chat_id {chat_id}: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint to receive updates from Telegram."""
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    update = request.get_json()
    
    # Process only message updates
    if "message" not in update:
        logger.info("Received update without a message object. Ignoring.")
        return jsonify({"status": "ok"}), 200
        
    message_data = update.get("message", {})
    chat_id = message_data.get("chat", {}).get("id")
    text = message_data.get("text")

    # Only process text messages
    if not chat_id or not text:
        logger.info("Message missing chat_id or text. Ignoring.")
        return jsonify({"status": "ok"}), 200

    logger.info(f"Received message from chat_id {chat_id}: {text}")

    try:
        # Pass to chatbot engine
        bot_response = process_message(str(chat_id), text)
        
        # Send reply back to Telegram
        if bot_response:
            send_message(chat_id, bot_response)
            
            # Database insert logic
            try:
                conn = psycopg2.connect(DATABASE_URL)
                cur = conn.cursor()
                
                # Insert user if they don't exist to prevent foreign key errors
                cur.execute("""
                    INSERT INTO users (phone, platform) 
                    VALUES (%s, %s)
                    ON CONFLICT (phone) DO NOTHING;
                """, (str(chat_id), "Telegram"))
                
                # Insert the message
                cur.execute("""
                    INSERT INTO messages (phone, message, response, platform) 
                    VALUES (%s, %s, %s, %s);
                """, (str(chat_id), text, bot_response, "Telegram"))
                
                conn.commit()
                print("Data saved")
            except psycopg2.Error as db_err:
                print(f"Database error: {db_err}")
                if 'conn' in locals() and conn:
                    conn.rollback()
            finally:
                if 'cur' in locals() and cur:
                    cur.close()
                if 'conn' in locals() and conn:
                    conn.close()

    except Exception as e:
        logger.error(f"Error processing message for chat_id {chat_id}: {e}", exc_info=True)

    # Always return 200 OK to Telegram so it doesn't retry
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return "Flask is running and ready to accept webhooks.", 200

if __name__ == '__main__':
    # Run server on port 5000
    app.run(host='0.0.0.0', port=5000)
