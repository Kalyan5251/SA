# hospital_whatsapp_automation.py
# Complete Single File Format
# Replies + Questions + Answers Flow for Big Multinational Hospital WhatsApp API

import enum
import json

WELCOME_MESSAGE = """
Welcome to GlobalCare International Hospital 🏥🌍

How may we assist you today?

1) Book Appointment
2) Reschedule / Cancel Appointment
3) Doctor Availability
4) Lab Reports
5) Billing & Insurance
6) Admission / Room Enquiry
7) Ambulance / Emergency
8) Pharmacy / Medicine Refill
9) Feedback / Complaint
10) Preventive Care Packages
11) International Patient Services
12) Talk to Human Support

Reply with a number to continue.
"""

FINAL_MESSAGE = """
Thank you for contacting GlobalCare International Hospital.
Our team will assist you shortly.
"""

MAIN_MENU = {
    "1": "Book Appointment",
    "2": "Reschedule / Cancel Appointment",
    "3": "Doctor Availability",
    "4": "Lab Reports",
    "5": "Billing & Insurance",
    "6": "Admission / Room Enquiry",
    "7": "Ambulance / Emergency",
    "8": "Pharmacy / Medicine Refill",
    "9": "Feedback / Complaint",
    "10": "Preventive Care Packages",
    "11": "International Patient Services",
    "12": "Talk to Human Support"
}

QUESTIONS = {
    "1": [
        "Please choose department:\n1) Cardiology\n2) Orthopedic\n3) Pediatrics\n4) Dermatology\n5) Neurology",
        "Choose preferred doctor or type ANY:",
        "Preferred date? (DD/MM/YYYY)",
        "Preferred time slot?",
        "Patient full name?",
        "Patient age?",
        "Registered mobile number?",
        "Insurance available? (Yes/No)"
    ],

    "2": [
        "Enter Appointment ID or Registered Mobile Number:",
        "Choose action:\n1) Reschedule\n2) Cancel",
        "Enter new preferred date:",
        "Enter new preferred time:"
    ],

    "3": [
        "Enter department or doctor name:",
        "Choose date to check availability:"
    ],

    "4": [
        "Enter Lab ID / UHID / Mobile Number:",
        "Choose report type:\n1) Blood Test\n2) Scan\n3) Full Health Checkup\n4) All Reports"
    ],

    "5": [
        "Choose billing option:\n1) Pending Bill\n2) Payment Receipt\n3) Insurance Claim\n4) Surgery Estimate",
        "Enter UHID / Mobile Number:"
    ],

    "6": [
        "Choose enquiry:\n1) Room Availability\n2) ICU Beds\n3) Admission Process\n4) Visitor Timings",
        "Preferred admission date?"
    ],

    "7": [
        "Emergency type?\n1) Cardiac\n2) Accident\n3) Stroke\n4) General Emergency",
        "Patient name?",
        "Current location?",
        "Need ambulance? (Yes/No)"
    ],

    "8": [
        "Choose option:\n1) Prescription Status\n2) Medicine Refill\n3) Home Delivery",
        "Enter Prescription ID / Mobile Number:"
    ],

    "9": [
        "Please rate your experience:\n1⭐ Poor\n2⭐ Fair\n3⭐ Good\n4⭐ Very Good\n5⭐ Excellent",
        "Please share comments (optional):"
    ],

    "10": [
        "Choose package:\n1) Executive Checkup\n2) Diabetes Screening\n3) Cardiac Checkup\n4) Women Wellness",
        "Preferred date?",
        "Patient name?",
        "Mobile number?"
    ],

    "11": [
        "Country of travel?",
        "Need service:\n1) Visa Assistance\n2) Airport Pickup\n3) Translator\n4) Treatment Package",
        "Patient name?",
        "Contact number?"
    ],

    "12": [
        "Please describe your requirement briefly:",
        "Preferred callback time?",
        "Contact number?"
    ]
}

AUTO_REPLIES = {
    "1": """
✅ Appointment Confirmed

Hospital: GlobalCare International Hospital
Department booked successfully.
You will receive doctor details shortly.

Reply CANCEL anytime to cancel.
""",

    "2": """
🔄 Appointment Updated Successfully.

Your latest schedule has been saved.
Thank you.
""",

    "3": """
👨⚕️ Available Doctors Found

Slots are open for your selected department.
Our scheduling team will message you shortly.
""",

    "4": """
📄 Your reports are ready.

Secure Download Link:
https://hospital.com/report/secure-link

For help reply SUPPORT.
""",

    "5": """
💳 Billing Details Generated.

Payment / insurance status is being processed.
Our billing desk will assist you shortly.
""",

    "6": """
🛏️ Admission Team Notified.

Room / bed availability details will be shared shortly.
""",

    "7": """
🚑 Emergency Request Received.

Response team alerted.
Please stay reachable on your phone.
""",

    "8": """
💊 Pharmacy Request Received.

Medicine team is processing your request now.
""",

    "9": """
🙏 Thank you for your feedback.

Your response helps us improve patient care.
""",

    "10": """
🩺 Preventive Care Booking Submitted.

Our wellness desk will confirm your slot soon.
""",

    "11": """
🌍 International Patient Desk Activated.

Our coordinator will contact you with next steps.
""",

    "12": """
👩💼 Human Support Request Received.

A hospital representative will contact you shortly.
"""
}

class State(enum.Enum):
    MAIN_MENU = 1
    QUESTIONNAIRE = 2
    COMPLETED = 3

class Session:
    def __init__(self):
        self.state = State.MAIN_MENU
        self.category = None
        self.question_index = 0
        self.answers = []

    def reset(self):
        self.state = State.MAIN_MENU
        self.category = None
        self.question_index = 0
        self.answers = []

class HospitalBot:
    def __init__(self):
        self.sessions = {}

    def get_session(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = Session()
        return self.sessions[user_id]

    def process_message(self, user_id, message):
        msg = message.strip().lower()
        session = self.get_session(user_id)

        if msg in ["/start", "hi", "hello", "menu"]:
            session.reset()
            return WELCOME_MESSAGE

        if session.state == State.MAIN_MENU:
            if msg in MAIN_MENU:
                session.category = msg
                session.state = State.QUESTIONNAIRE
                session.question_index = 0
                session.answers = []
                return QUESTIONS[msg][0]
            return WELCOME_MESSAGE

        elif session.state == State.QUESTIONNAIRE:
            session.answers.append({
                "question": QUESTIONS[session.category][session.question_index],
                "answer": message
            })

            session.question_index += 1

            if session.question_index < len(QUESTIONS[session.category]):
                return QUESTIONS[session.category][session.question_index]

            final_reply = AUTO_REPLIES[session.category]
            session.reset()
            return final_reply

        return WELCOME_MESSAGE


# Example Terminal Testing
if __name__ == "__main__":
    bot = HospitalBot()
    user_id = "demo_user"

    print(bot.process_message(user_id, "hi"))

    while True:
        user_input = input("You: ")
        print("Bot:", bot.process_message(user_id, user_input))
