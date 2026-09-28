import re

from backend.agent.memory import add_message
from backend.tools.security import security_check
from backend.tools.authorization import check_order_authorization
from backend.tools.order_status import get_order_status
from backend.tools.order_details import get_order_details
from backend.tools.knowledge_base import search_kb
from backend.automation.complaint import process_complaint


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def extract_order_id(message: str):
    """Extract order ID such as ORD-1005."""

    match = re.search(
        r"\bORD-\d+\b",
        message.upper()
    )

    if match:
        return match.group(0)

    return None


def is_greeting(message: str):
    """Detect common greetings."""

    text = message.lower().strip()

    greetings = [
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "heyy",
        "good morning",
        "good afternoon",
        "good evening",
        "namaste",
        "hola"
    ]

    if text in greetings:
        return True

    cleaned = (
        text
        .replace("!", "")
        .replace(".", "")
        .replace(",", "")
        .strip()
    )

    return cleaned in greetings


def is_thanks(message: str):
    """Detect thank-you messages."""

    text = message.lower().strip()

    thank_words = [
        "thanks",
        "thank you",
        "thankyou",
        "thank u",
        "thx"
    ]

    return any(
        word in text
        for word in thank_words
    )


def is_goodbye(message: str):
    """Detect goodbye messages."""

    text = message.lower().strip()

    goodbye_words = [
        "bye",
        "goodbye",
        "see you",
        "see ya",
        "good night"
    ]

    return any(
        word in text
        for word in goodbye_words
    )


def is_order_status_request(message: str):
    """Detect order status questions."""

    text = message.lower()

    keywords = [
        "where is my order",
        "where is order",
        "where's my order",
        "order status",
        "track my order",
        "track order",
        "delivery status",
        "order update",
        "when will my order arrive",
        "when will my order come"
    ]

    return any(
        keyword in text
        for keyword in keywords
    )


def is_order_details_request(message: str):
    """Detect order detail requests."""

    text = message.lower()

    keywords = [
        "order details",
        "what did i order",
        "show my order",
        "order information",
        "what is in my order",
        "items in my order",
        "order amount"
    ]

    return any(
        keyword in text
        for keyword in keywords
    )


def is_policy_request(message: str):
    """Detect restaurant policy questions."""

    text = message.lower()

    keywords = [
        "cancel",
        "cancellation",
        "refund",
        "refund policy",
        "payment policy",
        "delivery policy",
        "restaurant policy",
        "can i cancel",
        "money back"
    ]

    return any(
        keyword in text
        for keyword in keywords
    )


def is_complaint(message: str):
    """Detect complaints requiring possible escalation."""

    text = message.lower()

    keywords = [
        "payment deducted",
        "money deducted",
        "money was deducted",
        "payment failed",
        "order failed",
        "charged but",
        "wrong charge",
        "fraud",
        "urgent",
        "very late",
        "extremely late",
        "refund not received",
        "refund issue",
        "complaint",
        "problem with my order",
        "issue with my order"
    ]

    return any(
        keyword in text
        for keyword in keywords
    )


# ============================================================
# MAIN AGENT
# ============================================================

def process_message(
    session_id: str,
    customer_id: str,
    message: str
):
    """
    Main Restaurant AI Agent orchestration.

    User
      ↓
    Memory
      ↓
    Security
      ↓
    Conversation / Greeting
      ↓
    Complaint
      ↓
    Order Tools
      ↓
    Authorization
      ↓
    Knowledge Base
      ↓
    Response
    """

    # --------------------------------------------------------
    # CLEAN INPUT
    # --------------------------------------------------------

    message = message.strip()

    if not message:

        return {
            "type": "error",
            "message": "Please enter a message."
        }

    # --------------------------------------------------------
    # SAVE MESSAGE
    # --------------------------------------------------------

    add_message(
        session_id=session_id,
        role="user",
        content=message
    )

    # ========================================================
    # SECURITY
    # ========================================================

    security = security_check(message)

    if not security["allowed"]:

        response_message = security["message"]

        add_message(
            session_id=session_id,
            role="assistant",
            content=response_message
        )

        return {
            "type": "security_block",
            "message": response_message
        }

    # ========================================================
    # GREETING
    # ========================================================

    if is_greeting(message):

        response_message = (
            "Hello! 👋 Welcome to Restaurant AI Support.\n\n"
            "I can help you with:\n"
            "📦 Order status and order details\n"
            "🚚 Delivery questions\n"
            "💳 Payment problems\n"
            "💰 Refunds and cancellations\n"
            "🛠️ Technical issues\n\n"
            "How can I help you today?"
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=response_message
        )

        return {
            "type": "conversation",
            "message": response_message
        }

    # ========================================================
    # THANKS
    # ========================================================

    if is_thanks(message):

        response_message = (
            "You're very welcome! 😊\n\n"
            "If you need anything else, "
            "I'm here to help."
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=response_message
        )

        return {
            "type": "conversation",
            "message": response_message
        }

    # ========================================================
    # GOODBYE
    # ========================================================

    if is_goodbye(message):

        response_message = (
            "Goodbye! 👋\n\n"
            "Thank you for contacting Restaurant AI Support. "
            "Have a great day!"
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=response_message
        )

        return {
            "type": "conversation",
            "message": response_message
        }

    # ========================================================
    # COMPLAINT / ESCALATION
    # ========================================================

    if is_complaint(message):

        result = process_complaint(
            customer_id=customer_id,
            message=message
        )

        if result.get("success"):

            ticket = result.get(
                "ticket",
                {}
            )

            ticket_id = ticket.get(
                "ticket_id",
                "N/A"
            )

            category = result.get(
                "category",
                ticket.get(
                    "category",
                    "Support"
                )
            )

            priority = result.get(
                "priority",
                ticket.get(
                    "priority",
                    "Medium"
                )
            )

            response_message = (
                "I'm sorry you're experiencing this issue. "
                "I've escalated it to our support team.\n\n"
                f"🎫 Ticket: {ticket_id}\n"
                f"📂 Category: {category}\n"
                f"⚡ Priority: {priority}\n\n"
                "Our support team can now investigate the issue."
            )

            add_message(
                session_id=session_id,
                role="assistant",
                content=response_message
            )

            return {
                "type": "escalation",
                "message": response_message,
                "ticket_id": ticket_id,
                "category": category,
                "priority": priority
            }

        response_message = (
            "I couldn't create the support ticket right now. "
            "Please try again shortly."
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=response_message
        )

        return {
            "type": "error",
            "message": response_message
        }

    # ========================================================
    # ORDER STATUS
    # ========================================================

    if is_order_status_request(message):

        order_id = extract_order_id(message)

        if not order_id:

            response_message = (
                "Sure! 📦 I can check your order status.\n\n"
                "Please provide your order ID.\n\n"
                "For example: ORD-1005"
            )

            add_message(
                session_id=session_id,
                role="assistant",
                content=response_message
            )

            return {
                "type": "conversation",
                "message": response_message
            }

        # Authorization
        authorization = check_order_authorization(
            customer_id=customer_id,
            order_id=order_id
        )

        if not authorization.get("authorized"):

            response_message = (
                "🔐 I can't access that order because "
                "it is not associated with your customer account."
            )

            add_message(
                session_id=session_id,
                role="assistant",
                content=response_message
            )

            return {
                "type": "authorization_error",
                "message": response_message
            }

        # Get authoritative status
        result = get_order_status(order_id)

        if result.get("success"):

            status = result.get(
                "status",
                "Unknown"
            )

            estimated_delivery = result.get(
                "estimated_delivery",
                "Not available"
            )

            response_message = (
                f"📦 **Order {order_id}**\n\n"
                f"Current status: **{status}**\n"
                f"Estimated delivery: **{estimated_delivery}**"
            )

            add_message(
                session_id=session_id,
                role="assistant",
                content=response_message
            )

            return {
                "type": "order_status",
                "message": response_message,
                "order_id": order_id,
                "status": status,
                "estimated_delivery": estimated_delivery,
                "tool_used": "get_order_status"
            }

        response_message = (
            f"I couldn't find order **{order_id}**.\n\n"
            "Please check the order ID and try again."
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=response_message
        )

        return {
            "type": "tool_error",
            "message": response_message
        }

    # ========================================================
    # ORDER DETAILS
    # ========================================================

    if is_order_details_request(message):

        order_id = extract_order_id(message)

        if not order_id:

            response_message = (
                "Sure! 📋 I can show your order details.\n\n"
                "Please provide your order ID."
            )

            add_message(
                session_id=session_id,
                role="assistant",
                content=response_message
            )

            return {
                "type": "conversation",
                "message": response_message
            }

        authorization = check_order_authorization(
            customer_id=customer_id,
            order_id=order_id
        )

        if not authorization.get("authorized"):

            response_message = (
                "🔐 I can't access that order because "
                "it is not associated with your customer account."
            )

            add_message(
                session_id=session_id,
                role="assistant",
                content=response_message
            )

            return {
                "type": "authorization_error",
                "message": response_message
            }

        result = get_order_details(order_id)

        if result.get("success"):

            order = result.get(
                "order",
                {}
            )

            items = order.get(
                "items",
                []
            )

            if isinstance(items, list):

                items_text = ", ".join(
                    str(item)
                    for item in items
                )

            else:

                items_text = str(items)

            response_message = (
                f"📋 **Order {order_id}**\n\n"
                f"🏪 Restaurant: "
                f"{order.get('restaurant', 'N/A')}\n"
                f"🍽️ Items: {items_text}\n"
                f"💰 Amount: "
                f"₹{order.get('amount', 'N/A')}\n"
                f"📦 Status: "
                f"{order.get('status', 'N/A')}\n"
                f"💳 Payment: "
                f"{order.get('payment_status', 'N/A')}"
            )

            add_message(
                session_id=session_id,
                role="assistant",
                content=response_message
            )

            return {
                "type": "order_details",
                "message": response_message,
                "order_id": order_id,
                "tool_used": "get_order_details"
            }

        response_message = (
            f"I couldn't find order **{order_id}**."
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=response_message
        )

        return {
            "type": "tool_error",
            "message": response_message
        }

    # ========================================================
    # KNOWLEDGE BASE
    # ========================================================

    if is_policy_request(message):

        result = search_kb(message)

        if result.get("success"):

            results = result.get(
                "results",
                []
            )

            if results:

                best_result = results[0]

                content = best_result.get(
                    "content",
                    ""
                )

                response_message = (
                    "📚 **According to our restaurant policy:**\n\n"
                    f"{content}\n\n"
                    "If you need further assistance, "
                    "I can escalate the issue to support."
                )

                add_message(
                    session_id=session_id,
                    role="assistant",
                    content=response_message
                )

                return {
                    "type": "knowledge_base",
                    "message": response_message,
                    "tool_used": "search_knowledge_base"
                }

        response_message = (
            "I couldn't find a relevant policy in the "
            "knowledge base. I don't want to guess about "
            "the restaurant's policy."
        )

        add_message(
            session_id=session_id,
            role="assistant",
            content=response_message
        )

        return {
            "type": "knowledge_base_error",
            "message": response_message
        }

    # ========================================================
    # GENERAL RESPONSE
    # ========================================================

    response_message = (
        "I understand your request. 😊\n\n"
        "I can help you with:\n"
        "📦 Order tracking\n"
        "📋 Order details\n"
        "🚚 Delivery\n"
        "💰 Cancellation and refunds\n"
        "💳 Payment issues\n"
        "🛠️ Technical problems\n\n"
        "For example, you can ask:\n"
        "\"Where is my order ORD-1005?\""
    )

    add_message(
        session_id=session_id,
        role="assistant",
        content=response_message
    )

    return {
        "type": "conversation",
        "message": response_message
    }