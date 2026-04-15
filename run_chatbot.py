import sys
from chatbot_engine import HospitalBot

def main():
    bot = HospitalBot()
    user_id = "demo_user"
    
    print("\n--- Samriddhi Anveshana Chatbot Interactive Mode ---")
    print("Type 'exit' or 'quit' to stop.\n")
    
    # Start
    response = bot.process_message(user_id, "hi")
    print(f"Bot:\n{response}")
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
                
            response = bot.process_message(user_id, user_input)
            print(f"\nBot:\n{response}")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
