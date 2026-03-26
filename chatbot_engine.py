import enum
import psycopg2
import json
import os
import sys

raw_db_url = os.environ.get("DATABASE_URL", "postgresql://postgres.hrbndnvadhqfyncbryxw:Zz9oaKB2z5jUUPpC@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres")
DATABASE_URL = raw_db_url.replace("?pgbouncer=true", "").replace("\n", "").strip()

def log_interaction(user_id, user_message, bot_response, platform="Telegram"):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO users (phone, platform) 
            VALUES (%s, %s)
            ON CONFLICT (phone) DO NOTHING;
        """, (str(user_id), platform))
        
        cur.execute("""
            INSERT INTO messages (phone, message, response, platform) 
            VALUES (%s, %s, %s, %s);
        """, (str(user_id), user_message, bot_response, platform))
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error in log_interaction: {e}", file=sys.stderr, flush=True)

def save_lead(user_id, main_category, sub_category, answers):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO leads (user_id, main_category, sub_category, answers) 
            VALUES (%s, %s, %s, %s);
        """, (str(user_id), main_category, sub_category, json.dumps(answers)))
        
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error while saving lead: {e}", file=sys.stderr, flush=True)


WELCOME_MESSAGE = """Welcome to Samriddhi Anveshana. We provide professional services in:
1) IT Services & Digital Infrastructure
2) Digital Marketing
3) 24x7 Operational Support
4) Compliance & Operational Consulting
5) Financial Services
Please reply with the number to continue."""

FINAL_MESSAGE = "Thank you for contacting Samriddhi Anveshana. Our team will review your request and get in touch shortly."

MAIN_MENU = {
    "1": "IT Services & Digital Infrastructure",
    "2": "Digital Marketing",
    "3": "24x7 Operational Support",
    "4": "Compliance & Operational Consulting",
    "5": "Financial Services"
}

SUB_MENUS = {
    "1": {
        "1": "Hospital Management System (HMS)",
        "2": "EMR / EHR Systems",
        "3": "Cloud & Cybersecurity",
        "4": "Appointment Booking System",
        "5": "Telemedicine Integration"
    },
    "2": {
        "1": "Website Development",
        "2": "SEO Services",
        "3": "Google & Meta Ads",
        "4": "Social Media Management",
        "5": "Patient Engagement Campaigns"
    },
    "3": {
        "1": "Report an Issue",
        "2": "Request Technical Support",
        "3": "Monitoring Services"
    },
    "4": {
        "1": "Compliance Support",
        "2": "Audit Preparation",
        "3": "Workflow Optimization",
        "4": "Performance Analytics"
    },
    "5": {
        "1": "Payment Gateway Integration",
        "2": "Finance Automation Tools",
        "3": "Digital KYC Systems",
        "4": "Wealth Management Advisory"
    }
}

QUESTIONS = {
    "1": {  # IT Services & Digital Infrastructure
        "1": [ # HMS
            "Hospital / clinic name?",
            "Location?",
            "Number of beds / patients per day?",
            "Need billing & inventory modules? (Yes/No)",
            "Currently using any software? (Yes/No)",
            "Contact number?"
        ],
        "2": [ # EMR / EHR
            "Type of healthcare facility?",
            "Cloud-based or local system?",
            "Number of doctors / users?",
            "Need data migration from old system? (Yes/No)",
            "Compliance requirements? (NABH/NABL)",
            "Contact details?"
        ],
        "3": [ # Cloud & Cybersecurity
            "Current system type?",
            "Cloud hosting or security only?",
            "Previous security issues? (Yes/No)",
            "Approximate data size?",
            "Required security level? (Basic/Advanced)",
            "Contact number?"
        ],
        "4": [ # Appointment Booking System
            "Hospital / clinic name?",
            "Online booking needed? (Yes/No)",
            "Number of doctors?",
            "Preferred platform? (Web / App / Both)",
            "Need SMS / WhatsApp reminders? (Yes/No)",
            "Contact details?"
        ],
        "5": [ # Telemedicine Integration
            "Type of consultations? (Video / Audio / Both)",
            "Number of doctors?",
            "Payment integration needed? (Yes/No)",
            "Target audience (local / global)",
            "Existing system? (Yes/No)",
            "Contact number?"
        ]
    },
    "2": { # Digital Marketing
        "1": [ # Website Development
            "Business / hospital name?",
            "Already have a website? (Yes/No)",
            "Type of website? (Basic / Advanced / E-commerce)",
            "Required pages (Home, About, Services, etc.)?",
            "Booking / payment integration needed? (Yes/No)",
            "Contact details?"
        ],
        "2": [ # SEO Services
            "Website URL?",
            "Target location?",
            "Target keywords (if any)?",
            "Current traffic status (Low / Medium / High)?",
            "Competitors (if known)?",
            "Contact number?"
        ],
        "3": [ # Google & Meta Ads
            "Business type?",
            "Monthly ad budget?",
            "Target audience / location?",
            "Goal? (Leads / Traffic / Sales)",
            "Previous ads experience? (Yes/No)",
            "Contact details?"
        ],
        "4": [ # Social Media Management
            "Platforms (Instagram / Facebook / etc.)?",
            "Current followers?",
            "Posting frequency needed?",
            "Content type? (Reels / Posts / Both)",
            "Branding requirements?",
            "Contact number?"
        ],
        "5": [ # Patient Engagement Campaigns
            "Target audience type?",
            "Campaign goal?",
            "Preferred channel (WhatsApp / SMS / Email)",
            "Campaign duration?",
            "Need automation? (Yes/No)",
            "Contact details?"
        ]
    },
    "3": { # 24x7 Operational Support
        "1": [ # Report an Issue
            "Issue type?",
            "System affected?",
            "When did it occur?",
            "Urgency level? (Low / Medium / High)",
            "Screenshot (if possible)?",
            "Contact number?"
        ],
        "2": [ # Request Technical Support
            "Type of support needed?",
            "System details?",
            "Preferred time?",
            "Issue description?",
            "Priority level?",
            "Contact details?"
        ],
        "3": [ # Monitoring Services
            "What system needs monitoring?",
            "Current setup?",
            "Alert preferences?",
            "Reporting frequency?",
            "Number of systems?",
            "Contact number?"
        ]
    },
    "4": { # Compliance & Operational Consulting
        "1": [ # Compliance Support
            "Hospital type?",
            "Required certification (NABH / NABL)",
            "Current compliance status?",
            "Documentation available? (Yes/No)",
            "Timeline?",
            "Contact details?"
        ],
        "2": [ # Audit Preparation
            "Audit type?",
            "Scheduled date?",
            "Current readiness level?",
            "Required documentation?",
            "Need training? (Yes/No)",
            "Contact number?"
        ],
        "3": [ # Workflow Optimization
            "Department to optimize?",
            "Current challenges?",
            "Expected improvements?",
            "Number of staff?",
            "Tools currently used?",
            "Contact details?"
        ],
        "4": [ # Performance Analytics
            "What metrics do you track?",
            "Need dashboard? (Yes/No)",
            "Data source?",
            "Reporting frequency?",
            "Goals?",
            "Contact number?"
        ]
    },
    "5": { # Financial Services
        "1": [ # Payment Gateway Integration
            "Business / company name?",
            "Type of business? (Retail / Healthcare / E-commerce / Other)",
            "Expected monthly transaction volume?",
            "Need UPI / card / wallet support? (specify)",
            "Existing website or app? (Yes/No)",
            "Contact details?"
        ],
        "2": [ # Finance Automation Tools
            "Business type and size?",
            "Which processes to automate? (Invoicing / Payroll / Reconciliation)",
            "Current accounting software? (Tally / Zoho / Other / None)",
            "Number of transactions per month (approx.)?",
            "Need staff training? (Yes/No)",
            "Contact number?"
        ],
        "3": [ # Digital KYC Systems
            "Organisation type? (NBFC / Bank / Fintech / Healthcare)",
            "Expected number of KYC verifications per month?",
            "Document types needed? (Aadhaar / PAN / Passport / Other)",
            "Need video KYC? (Yes/No)",
            "Existing system to integrate with? (Yes/No)",
            "Contact details?"
        ],
        "4": [ # Wealth Management Advisory
            "Individual or corporate client?",
            "Investment goal? (Wealth growth / Tax saving / Retirement / Other)",
            "Risk appetite? (Low / Medium / High)",
            "Approximate investment amount or monthly SIP budget?",
            "Existing investments? (Yes/No)",
            "Contact number?"
        ]
    }
}

class State(enum.Enum):
    MAIN_MENU = 1
    SUB_MENU = 2
    QUESTIONNAIRE = 3
    COMPLETED = 4

class ChatbotSession:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state = State.MAIN_MENU
        self.main_category = None
        self.sub_category = None
        self.question_index = 0
        self.answers = []

    def reset(self):
        self.state = State.MAIN_MENU
        self.main_category = None
        self.sub_category = None
        self.question_index = 0
        self.answers = []

class SamriddhiChatbot:
    def __init__(self):
        self.sessions = {} # user_id -> ChatbotSession

    def get_session(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = ChatbotSession(user_id)
        return self.sessions[user_id]

    def _format_sub_menu(self, cat_id):
        cat_name = MAIN_MENU[cat_id]
        opts = SUB_MENUS[cat_id]
        msg = f"{cat_name}\nPlease reply with the number to select an option:\n"
        for k, v in opts.items():
            msg += f"{k}) {v}\n"
        msg += "0) Back to Main Menu"
        return msg

    def process_message(self, user_id, message):
        bot_response = self._generate_response(user_id, message)
        log_interaction(user_id, message, bot_response)
        return bot_response

    def _generate_response(self, user_id, message):
        message = message.strip()
        session = self.get_session(user_id)

        # Allow resetting / going back
        if message == "0" and session.state in [State.SUB_MENU, State.QUESTIONNAIRE]:
            if session.state == State.SUB_MENU:
                session.reset()
                return WELCOME_MESSAGE
            elif session.state == State.QUESTIONNAIRE:
                if session.question_index == 0:
                    # Going back from Q1 takes us back to the sub menu
                    session.state = State.SUB_MENU
                    session.sub_category = None
                    return self._format_sub_menu(session.main_category)
                else:
                    # They might type 0 as an answer, so we don't automatically treat it as back,
                    # but if we wanted to support 'Back to menu' during questionnaire we could.
                    # As per standard bot design, let's treat "0" or "Back" as back to Main Menu.
                    pass
        
        if message.lower() in ['back', 'back to menu']:
            session.reset()
            return WELCOME_MESSAGE
            
        if message.lower() == '/start' or message.lower() == 'hi' or message.lower() == 'hello':
            session.reset()
            return WELCOME_MESSAGE

        if session.state == State.MAIN_MENU:
            if message in MAIN_MENU:
                session.main_category = message
                session.state = State.SUB_MENU
                return self._format_sub_menu(session.main_category)
            else:
                return f"Invalid option. Please reply with a number between 1 and {len(MAIN_MENU)}.\n\n" + WELCOME_MESSAGE

        elif session.state == State.SUB_MENU:
            opts = SUB_MENUS[session.main_category]
            if message in opts:
                session.sub_category = message
                session.state = State.QUESTIONNAIRE
                session.question_index = 0
                session.answers = []
                question = QUESTIONS[session.main_category][session.sub_category][0]
                return f"Great! Let's get some details for {opts[message]}.\n\nQ1: {question}"
            else:
                return f"Invalid option. Please reply with a number between 1 and {len(opts)}.\n\n" + self._format_sub_menu(session.main_category)

        elif session.state == State.QUESTIONNAIRE:
            # Capture answer
            q_list = QUESTIONS[session.main_category][session.sub_category]
            session.answers.append({
                "question": q_list[session.question_index],
                "answer": message
            })
            
            session.question_index += 1
            
            if session.question_index < len(q_list):
                # Ask next question
                next_q = q_list[session.question_index]
                return f"Q{session.question_index + 1}: {next_q}"
            else:
                # Flow completed
                session.state = State.COMPLETED
                
                # Save the lead details to the database before resetting
                main_cat_name = MAIN_MENU[session.main_category]
                sub_cat_name = SUB_MENUS[session.main_category][session.sub_category]
                
                save_lead(session.user_id, main_cat_name, sub_cat_name, session.answers)
                
                session.reset()
                return FINAL_MESSAGE

        elif session.state == State.COMPLETED:
            # Should not technically happen since it resets, but just in case
            session.reset()
            return WELCOME_MESSAGE

        return WELCOME_MESSAGE
