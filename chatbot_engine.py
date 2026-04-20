# chatbot_engine.py
# GlobalCare International Hospital — Enterprise WhatsApp Automation Bot
# Full single-file format with session-based conversation flow

import enum
import random
import string
from datetime import datetime

# ─────────────────────────────────────────────
# HOSPITAL CONFIGURATION
# ─────────────────────────────────────────────

HOSPITAL_NAME = "GlobalCare International Hospital"
HOSPITAL_PHONE = "+91 1800-425-4321"
HOSPITAL_EMAIL = "care@globalcare.in"
HOSPITAL_WEBSITE = "www.globalcare.in"

DEPARTMENTS = {
    "1": "Cardiology",
    "2": "Orthopedic",
    "3": "Neurology",
    "4": "Pediatrics",
    "5": "Dermatology",
    "6": "Oncology",
    "7": "Gastroenterology",
    "8": "IVF & Fertility"
}

DOCTOR_MAP = {
    "Cardiology":        "Dr. Arjun Sharma",
    "Orthopedic":        "Dr. Suresh Rao",
    "Neurology":         "Dr. Vikram Mehta",
    "Pediatrics":        "Dr. Priya Nair",
    "Dermatology":       "Dr. Zara Khan",
    "Oncology":          "Dr. Rajesh Patel",
    "Gastroenterology":  "Dr. Srinivas Reddy",
    "IVF & Fertility":   "Dr. Anita Krishnan"
}

HEALTH_PACKAGES = {
    "1": "Executive Full Body Checkup",
    "2": "Diabetes Screening Package",
    "3": "Cardiac Wellness Checkup",
    "4": "Women Wellness Package",
    "5": "Senior Citizen Package",
    "6": "Pre-Marital Health Checkup"
}

INTL_SERVICES = {
    "1": "Visa Invitation Letter",
    "2": "Airport Pickup & Transfers",
    "3": "Medical Interpreter",
    "4": "Treatment Package & Estimate",
    "5": "Concierge & Hotel Assistance"
}

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────

def generate_booking_id(prefix="GC"):
    """Generate a unique alphanumeric booking/ticket ID."""
    suffix = ''.join(random.choices(string.digits, k=5))
    return f"{prefix}{suffix}"

def assign_doctor(department_choice):
    """Return the assigned doctor for a given department key or name."""
    dept_name = DEPARTMENTS.get(department_choice, department_choice)
    return DOCTOR_MAP.get(dept_name, "Consulting Specialist"), dept_name

def format_department_menu():
    lines = ["Please select your department:\n"]
    for k, v in DEPARTMENTS.items():
        lines.append(f"  {k}) {v}")
    return "\n".join(lines)

def format_package_menu():
    lines = ["Please select a health package:\n"]
    for k, v in HEALTH_PACKAGES.items():
        lines.append(f"  {k}) {v}")
    return "\n".join(lines)

def format_intl_menu():
    lines = ["Please select the service you need:\n"]
    for k, v in INTL_SERVICES.items():
        lines.append(f"  {k}) {v}")
    return "\n".join(lines)

def format_confirmation(template, **kwargs):
    """Fill a confirmation template with dynamic values."""
    return template.format(**kwargs)

# ─────────────────────────────────────────────
# MESSAGES
# ─────────────────────────────────────────────

WELCOME_MESSAGE = f"""🏥 *Welcome to {HOSPITAL_NAME}*

We are here to assist you 24×7.
Please choose an option below:

  1️⃣  Book Appointment
  2️⃣  Reschedule / Cancel Appointment
  3️⃣  Doctor Availability
  4️⃣  Lab Reports
  5️⃣  Billing & Insurance
  6️⃣  Admission / Room Enquiry
  7️⃣  Ambulance / Emergency
  8️⃣  Pharmacy / Medicine Refill
  9️⃣  Feedback / Complaint
  🔟  Preventive Health Packages
  1️⃣1️⃣  International Patient Services
  1️⃣2️⃣  Talk to Human Support

Reply with a *number* to continue.
"""

RETURNING_USER_MESSAGE = f"""👋 *Welcome back to {HOSPITAL_NAME}!*

How may we assist you today?

  1️⃣  Book Appointment
  2️⃣  Reschedule / Cancel Appointment
  3️⃣  Doctor Availability
  4️⃣  Lab Reports
  5️⃣  Billing & Insurance
  6️⃣  Admission / Room Enquiry
  7️⃣  Ambulance / Emergency
  8️⃣  Pharmacy / Medicine Refill
  9️⃣  Feedback / Complaint
  🔟  Preventive Health Packages
  1️⃣1️⃣  International Patient Services
  1️⃣2️⃣  Talk to Human Support

Reply with a *number* to continue.
"""

INVALID_INPUT = (
    "⚠️ Sorry, I didn't understand that.\n"
    "Please reply with a valid option number, or type *MENU* to return to the main menu."
)

MAIN_MENU_KEYS = {str(i) for i in range(1, 13)}

# ─────────────────────────────────────────────
# QUESTION FLOWS  (one list per module)
# ─────────────────────────────────────────────

QUESTIONS = {
    # 1 — Book Appointment
    "1": [
        format_department_menu(),
        "👨‍⚕️ Preferred doctor? (Type doctor name or reply *ANY* for next available):",
        "📅 Preferred date? *(DD/MM/YYYY)*",
        "🕐 Preferred time slot? *(e.g. 10:00 AM, 2:30 PM)*",
        "👤 Patient's full name?",
        "🔢 Patient's age?",
        "📱 Registered mobile number?",
        "🛡️ Do you have insurance? *(Yes / No)*"
    ],

    # 2 — Reschedule / Cancel
    "2": [
        "📋 Please enter your *Appointment ID* or *Registered Mobile Number*:",
        "Choose action:\n  1) Reschedule\n  2) Cancel",
        "📅 New preferred date? *(DD/MM/YYYY)*",
        "🕐 New preferred time slot?"
    ],

    # 3 — Doctor Availability
    "3": [
        format_department_menu(),
        "📅 Which date would you like to check? *(DD/MM/YYYY)*"
    ],

    # 4 — Lab Reports
    "4": [
        "🔬 Please enter your *Lab ID / UHID / Mobile Number*:",
        "Choose report type:\n  1) Blood Test Report\n  2) Radiology / Scan\n  3) Full Health Checkup\n  4) All Reports"
    ],

    # 5 — Billing & Insurance
    "5": [
        "💳 Choose billing option:\n  1) View Pending Bill\n  2) Download Payment Receipt\n  3) Insurance Claim Status\n  4) Surgery Cost Estimate",
        "🔢 Please enter your *UHID / Mobile Number*:"
    ],

    # 6 — Admission / Room Enquiry
    "6": [
        "🛏️ Choose enquiry type:\n  1) Room / Ward Availability\n  2) ICU / NICU Beds\n  3) Admission Process\n  4) Visitor Timings & Policy",
        "📅 Expected admission date? *(DD/MM/YYYY)*",
        "👤 Patient's full name?"
    ],

    # 7 — Ambulance / Emergency
    "7": [
        "🚨 Emergency type:\n  1) Cardiac Emergency\n  2) Road Accident / Trauma\n  3) Stroke / Neurological\n  4) Maternity Emergency\n  5) Other Emergency",
        "👤 Patient's name?",
        "📍 Current location / address?",
        "🚑 Do you need an ambulance? *(Yes / No)*"
    ],

    # 8 — Pharmacy / Medicine Refill
    "8": [
        "💊 Choose option:\n  1) Check Prescription Status\n  2) Request Medicine Refill\n  3) Home Delivery Order",
        "🔢 Enter *Prescription ID / Mobile Number*:"
    ],

    # 9 — Feedback / Complaint
    "9": [
        "⭐ Please rate your overall experience:\n  1️⃣  Poor\n  2️⃣  Fair\n  3️⃣  Good\n  4️⃣  Very Good\n  5️⃣  Excellent",
        "📝 Please share your comments or suggestions *(or type SKIP)*:"
    ],

    # 10 — Preventive Health Packages
    "10": [
        format_package_menu(),
        "📅 Preferred date? *(DD/MM/YYYY)*",
        "👤 Patient's full name?",
        "📱 Mobile number?"
    ],

    # 11 — International Patient Services
    "11": [
        "🌍 Which country are you traveling from?",
        format_intl_menu(),
        "👤 Patient's full name?",
        "📱 International contact number? *(with country code)*"
    ],

    # 12 — Human Support
    "12": [
        "📝 Please briefly describe your requirement:",
        "🕐 Preferred callback time? *(e.g. 10 AM – 12 PM)*",
        "📱 Your contact number?"
    ]
}

# ─────────────────────────────────────────────
# CONFIRMATION TEMPLATES
# ─────────────────────────────────────────────

CONFIRMATIONS = {
    "1": """✅ *Appointment Confirmed*

🏥 Hospital: {hospital}
👤 Patient: {patient_name}
🏷️ Age: {age}
🏢 Department: {department}
👨‍⚕️ Doctor: {doctor}
📅 Date: {date}
🕐 Time: {time}
🛡️ Insurance: {insurance}
🔖 Booking ID: *{booking_id}*

Please arrive *15 minutes* before your appointment.
Carry a valid photo ID and insurance card (if applicable).

Reply *CANCEL* anytime to cancel your appointment.
📞 Helpline: {helpline}""",

    "2": """🔄 *Appointment Updated Successfully*

🔖 Reference ID: *{booking_id}*
📅 New Date: {date}
🕐 New Time: {time}

Your updated schedule has been saved.
You will receive a confirmation SMS shortly.
📞 For help: {helpline}""",

    "3": """👨‍⚕️ *Doctor Availability Checked*

🏢 Department: {department}
👨‍⚕️ Doctor: {doctor}
📅 Date: {date}
🟢 Status: Slots Available

To book an appointment, reply *1*.
📞 Helpline: {helpline}""",

    "4": """📄 *Lab Report Request Received*

🔖 Report Request ID: *{booking_id}*
📋 Report Type: {report_type}
🔗 Secure Access: https://globalcare.in/reports/{booking_id}

For assistance reply *SUPPORT*.
📞 Helpline: {helpline}""",

    "5": """💳 *Billing Case Registered*

🔖 Case ID: *{booking_id}*
📝 Request: {billing_option}
👤 UHID / Mobile: {uhid}

Our billing desk will assist you within *2 business hours*.
📞 Billing Helpline: {helpline}""",

    "6": """🛏️ *Admission Enquiry Registered*

🔖 Enquiry ID: *{booking_id}*
📋 Type: {enquiry_type}
👤 Patient: {patient_name}
📅 Expected Date: {date}

Our admissions team will contact you shortly.
📞 Helpline: {helpline}""",

    "7": """🚨 *EMERGENCY REQUEST RECEIVED*

🔖 Emergency Ticket ID: *{booking_id}*
⚠️ Type: {emergency_type}
👤 Patient: {patient_name}
📍 Location: {location}
🚑 Ambulance: {ambulance}

Our response team has been *immediately alerted*.
Please keep your phone reachable.
📞 Emergency Hotline: {helpline}""",

    "8": """💊 *Pharmacy Request Submitted*

🔖 Request ID: *{booking_id}*
📋 Service: {service_type}
🔢 Prescription Ref: {prescription_id}

Our pharmacy team will process your request within *1 hour*.
📞 Pharmacy Helpline: {helpline}""",

    "9": """🙏 *Thank You for Your Feedback!*

⭐ Rating: {rating}
🔖 Feedback ID: *{booking_id}*

Your response helps us continuously improve patient care.
If you have an urgent complaint, reply *SUPPORT*.
📞 Patient Experience: {helpline}""",

    "10": """🩺 *Health Package Booking Confirmed*

🔖 Booking ID: *{booking_id}*
📦 Package: {package}
👤 Patient: {patient_name}
📅 Date: {date}
📱 Mobile: {mobile}

Our wellness desk will confirm your time slot via SMS.
Please arrive *30 minutes* before your scheduled time.
📞 Wellness Desk: {helpline}""",

    "11": """🌍 *International Patient Desk Activated*

🔖 Reference ID: *{booking_id}*
🌐 Country: {country}
📋 Service: {service}
👤 Patient: {patient_name}
📱 Contact: {contact}

Our international coordinator will reach you within *24 hours*.
📧 Email: {email}
🌐 Website: {website}""",

    "12": """👩‍💼 *Human Support Request Logged*

🔖 Support Ticket ID: *{booking_id}*
📝 Requirement: {requirement}
🕐 Callback Time: {callback_time}
📱 Contact: {contact}

A dedicated hospital representative will call you at your preferred time.
📞 Direct Helpline: {helpline}"""
}

STAR_RATINGS = {
    "1": "1⭐ Poor",
    "2": "2⭐ Fair",
    "3": "3⭐ Good",
    "4": "4⭐ Very Good",
    "5": "5⭐ Excellent"
}

BILLING_OPTIONS = {
    "1": "Pending Bill View",
    "2": "Payment Receipt Download",
    "3": "Insurance Claim Status",
    "4": "Surgery Cost Estimate"
}

EMERGENCY_TYPES = {
    "1": "Cardiac Emergency",
    "2": "Road Accident / Trauma",
    "3": "Stroke / Neurological",
    "4": "Maternity Emergency",
    "5": "General Emergency"
}

PHARMACY_SERVICES = {
    "1": "Prescription Status Check",
    "2": "Medicine Refill Request",
    "3": "Home Delivery Order"
}

ENQUIRY_TYPES = {
    "1": "Room / Ward Availability",
    "2": "ICU / NICU Beds",
    "3": "Admission Process",
    "4": "Visitor Timings & Policy"
}

# ─────────────────────────────────────────────
# STATE MACHINE
# ─────────────────────────────────────────────

class State(enum.Enum):
    MAIN_MENU    = 1
    QUESTIONNAIRE = 2
    COMPLETED    = 3


class Session:
    def __init__(self):
        self.state          = State.MAIN_MENU
        self.category       = None
        self.question_index = 0
        self.answers        = []
        self.visit_count    = 0  # Track returning users

    def reset(self):
        self.state          = State.MAIN_MENU
        self.category       = None
        self.question_index = 0
        self.answers        = []


# ─────────────────────────────────────────────
# CONFIRMATION BUILDER
# ─────────────────────────────────────────────

def build_confirmation(category, answers):
    """Build a dynamic confirmation message based on collected answers."""
    bid = generate_booking_id()
    hl  = HOSPITAL_PHONE

    a = answers  # shorthand

    def get(i, default="N/A"):
        return a[i]["answer"] if i < len(a) else default

    if category == "1":
        dept_key  = get(0)
        doctor, dept_name = assign_doctor(dept_key)
        doctor_input = get(1)
        if doctor_input.upper() != "ANY":
            doctor = doctor_input
        return format_confirmation(
            CONFIRMATIONS["1"],
            hospital     = HOSPITAL_NAME,
            patient_name = get(4),
            age          = get(5),
            department   = dept_name,
            doctor       = doctor,
            date         = get(2),
            time         = get(3),
            insurance    = get(7),
            booking_id   = bid,
            helpline     = hl
        )

    elif category == "2":
        return format_confirmation(
            CONFIRMATIONS["2"],
            booking_id = bid,
            date       = get(2),
            time       = get(3),
            helpline   = hl
        )

    elif category == "3":
        dept_key = get(0)
        doctor, dept_name = assign_doctor(dept_key)
        return format_confirmation(
            CONFIRMATIONS["3"],
            department = dept_name,
            doctor     = doctor,
            date       = get(1),
            helpline   = hl
        )

    elif category == "4":
        report_map = {"1": "Blood Test", "2": "Radiology / Scan",
                      "3": "Full Health Checkup", "4": "All Reports"}
        rt = report_map.get(get(1), get(1))
        return format_confirmation(
            CONFIRMATIONS["4"],
            booking_id  = bid,
            report_type = rt,
            helpline    = hl
        )

    elif category == "5":
        bo = BILLING_OPTIONS.get(get(0), get(0))
        return format_confirmation(
            CONFIRMATIONS["5"],
            booking_id     = bid,
            billing_option = bo,
            uhid           = get(1),
            helpline       = hl
        )

    elif category == "6":
        et = ENQUIRY_TYPES.get(get(0), get(0))
        return format_confirmation(
            CONFIRMATIONS["6"],
            booking_id   = bid,
            enquiry_type = et,
            patient_name = get(2),
            date         = get(1),
            helpline     = hl
        )

    elif category == "7":
        etype = EMERGENCY_TYPES.get(get(0), get(0))
        return format_confirmation(
            CONFIRMATIONS["7"],
            booking_id     = generate_booking_id("EM"),
            emergency_type = etype,
            patient_name   = get(1),
            location       = get(2),
            ambulance      = get(3),
            helpline       = hl
        )

    elif category == "8":
        stype = PHARMACY_SERVICES.get(get(0), get(0))
        return format_confirmation(
            CONFIRMATIONS["8"],
            booking_id      = generate_booking_id("PH"),
            service_type    = stype,
            prescription_id = get(1),
            helpline        = hl
        )

    elif category == "9":
        rating = STAR_RATINGS.get(get(0), get(0))
        return format_confirmation(
            CONFIRMATIONS["9"],
            booking_id = generate_booking_id("FB"),
            rating     = rating,
            helpline   = hl
        )

    elif category == "10":
        pkg = HEALTH_PACKAGES.get(get(0), get(0))
        return format_confirmation(
            CONFIRMATIONS["10"],
            booking_id   = bid,
            package      = pkg,
            patient_name = get(2),
            date         = get(1),
            mobile       = get(3),
            helpline     = hl
        )

    elif category == "11":
        svc = INTL_SERVICES.get(get(1), get(1))
        return format_confirmation(
            CONFIRMATIONS["11"],
            booking_id = bid,
            country    = get(0),
            service    = svc,
            patient_name = get(2),
            contact    = get(3),
            email      = HOSPITAL_EMAIL,
            website    = HOSPITAL_WEBSITE
        )

    elif category == "12":
        return format_confirmation(
            CONFIRMATIONS["12"],
            booking_id    = generate_booking_id("SP"),
            requirement   = get(0),
            callback_time = get(1),
            contact       = get(2),
            helpline      = hl
        )

    return "✅ Your request has been submitted. Our team will contact you shortly."


# ─────────────────────────────────────────────
# MAIN BOT CLASS
# ─────────────────────────────────────────────

class HospitalBot:
    def __init__(self):
        self.sessions = {}

    def get_session(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = Session()
        return self.sessions[user_id]

    def process_message(self, user_id, message):
        """Main entry point. Returns a reply string for the given user message."""
        msg     = message.strip()
        msg_low = msg.lower()
        session = self.get_session(user_id)

        # ── Global triggers ────────────────────────────────────────────
        if msg_low in ["/start", "hi", "hello", "hey", "start", "menu", "main menu"]:
            session.visit_count += 1
            session.reset()
            if session.visit_count > 1:
                return RETURNING_USER_MESSAGE
            return WELCOME_MESSAGE

        if msg_low == "cancel":
            session.reset()
            return (
                "❌ Your current request has been cancelled.\n\n"
                "Type *MENU* to return to the main menu or say *Hi* to start over."
            )

        if msg_low in ["support", "human"]:
            session.reset()
            session.category = "12"
            session.state    = State.QUESTIONNAIRE
            session.question_index = 0
            session.answers  = []
            return QUESTIONS["12"][0]

        # ── Main menu ─────────────────────────────────────────────────
        if session.state == State.MAIN_MENU:
            if msg in MAIN_MENU_KEYS:
                session.category       = msg
                session.state          = State.QUESTIONNAIRE
                session.question_index = 0
                session.answers        = []
                return QUESTIONS[msg][0]

            # Unrecognised input at main menu
            return INVALID_INPUT

        # ── Questionnaire flow ────────────────────────────────────────
        elif session.state == State.QUESTIONNAIRE:
            # Record this answer
            session.answers.append({
                "question": QUESTIONS[session.category][session.question_index],
                "answer":   msg
            })
            session.question_index += 1

            # More questions remain?
            if session.question_index < len(QUESTIONS[session.category]):
                return QUESTIONS[session.category][session.question_index]

            # All answers collected — build dynamic confirmation
            confirmation = build_confirmation(session.category, session.answers)
            session.reset()
            return confirmation

        # ── Fallback ──────────────────────────────────────────────────
        return INVALID_INPUT


# ─────────────────────────────────────────────
# TERMINAL TEST MODE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    bot     = HospitalBot()
    user_id = "demo_user"

    print("\n" + "=" * 60)
    print(f"  {HOSPITAL_NAME}")
    print("  WhatsApp Bot — Terminal Test Mode")
    print("=" * 60)
    print(bot.process_message(user_id, "hi"))

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            reply = bot.process_message(user_id, user_input)
            print(f"\nBot:\n{reply}\n")
        except KeyboardInterrupt:
            print("\n\nSession ended. Goodbye!")
            break
