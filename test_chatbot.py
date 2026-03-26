from chatbot_engine import SamriddhiChatbot, State

def test_flow_hms():
    bot = SamriddhiChatbot()
    user_id = "user1"
    
    # Start
    res = bot.process_message(user_id, "hi")
    assert "Welcome to Samriddhi Anveshana" in res
    
    # Select IT Services
    res = bot.process_message(user_id, "1")
    assert "IT Services & Digital Infrastructure" in res
    assert "1) Hospital Management System (HMS)" in res
    
    # Test valid sub-menu option
    res = bot.process_message(user_id, "1")
    assert "Q1: Hospital / clinic name?" in res
    
    # Answer 6 questions
    res = bot.process_message(user_id, "Apollo Hospital")
    assert "Q2: Location?" in res
    res = bot.process_message(user_id, "Delhi")
    assert "Q3: Number of beds" in res
    res = bot.process_message(user_id, "500")
    assert "Q4: Need billing" in res
    res = bot.process_message(user_id, "Yes")
    assert "Q5: Currently using" in res
    res = bot.process_message(user_id, "No")
    assert "Q6: Contact number?" in res
    
    # Final answer
    res = bot.process_message(user_id, "9876543210")
    assert "Thank you for contacting Samriddhi Anveshana" in res
    
    # Check that session was reset
    session = bot.get_session(user_id)
    assert session.state == State.MAIN_MENU
    
    print("Test passed successfully!")

def test_go_back():
    bot = SamriddhiChatbot()
    user_id = "user2"
    bot.process_message(user_id, "hi")
    bot.process_message(user_id, "2") # Digital Marketing
    
    # User decides to go back
    res = bot.process_message(user_id, "0")
    assert "Welcome to Samriddhi Anveshana" in res
    
    # Select again 3
    res = bot.process_message(user_id, "3")
    assert "24x7 Operational Support" in res
    
    # Select item 1
    res = bot.process_message(user_id, "1")
    assert "Q1:" in res
    
    # Answer Q1
    res = bot.process_message(user_id, "Login failed")
    assert "Q2:" in res
    
    print("Go back test passed successfully!")

if __name__ == "__main__":
    test_flow_hms()
    test_go_back()
