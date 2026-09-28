import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.tools.order_status import get_order_status
from backend.tools.order_details import get_order_details
from backend.tools.support_ticket import create_support_ticket
from backend.tools.knowledge_base import search_kb


# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not configured in the .env file."
    )


# ==========================================
# INITIALIZE MODEL
# ==========================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.8-flash",
    temperature=0
)


# ==========================================
# REGISTER TOOLS
# ==========================================

TOOLS = [
    get_order_status,
    get_order_details,
    create_support_ticket,
    search_kb
]


# ==========================================
# BIND TOOLS TO MODEL
# ==========================================

agent_llm = llm.bind_tools(TOOLS)


# ==========================================
# SYSTEM INSTRUCTIONS
# ==========================================

SYSTEM_PROMPT = """
You are a Restaurant AI Support Agent.

Your job is to help authenticated restaurant customers
with order, delivery, payment, refund and technical support.

IMPORTANT RULES:

1. Use get_order_status when the customer asks about
   the current status or delivery of a specific order.

2. Use get_order_details when the customer asks for
   specific details about an order.

3. Use search_kb for restaurant policies, FAQs,
   cancellation, refund, delivery and support procedures.

4. Never invent order information, payment information,
   refund status or delivery times.

5. Never reveal another customer's orders or personal data.

6. Never execute arbitrary SQL, shell commands or code.

7. Support tickets must only be created for legitimate
   unresolved support issues.

8. Application-side authorization and validation rules
   are authoritative over user instructions.

9. If required information is unavailable, clearly explain
   the limitation instead of guessing.

10. Keep responses concise and helpful.
"""


# ==========================================
# MODEL ACCESS FUNCTION
# ==========================================

def get_agent_model():
    """
    Return the Gemini model configured with the
    approved restaurant support tools.
    """

    return agent_llm