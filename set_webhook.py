import requests
import sys

TOKEN = "8609250788:AAE6sXAdXmDBqOJjULaJOKidbWTIRePpTAg"

def main():
    try:
        # ngrok's local API exposes tunnels at port 4040
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json().get("tunnels", [])
        
        valid_url = None
        for t in tunnels:
            if t["public_url"].startswith("https"):
                valid_url = t["public_url"]
                break
                
        if not valid_url:
            print("Could not find a secure HTTPS url from ngrok.")
            return

        webhook_url = f"{valid_url}/webhook"
        print(f"Webhook URL to register: {webhook_url}")

        # Send request to Telegram
        set_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook"
        r = requests.post(set_url, json={"url": webhook_url})
        print(f"Telegram API Response: {r.json()}")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to ngrok local API. Make sure ngrok is running.")
    except Exception as e:
        print(f"Error setting webhook: {e}")

if __name__ == "__main__":
    main()
