from backend.tools.support_ticket import create_support_ticket


# ==========================================
# ALLOWED CATEGORIES
# ==========================================

ALLOWED_CATEGORIES = {
    "Payment",
    "Order",
    "Delivery",
    "Refund",
    "Technical"
}


ALLOWED_PRIORITIES = {
    "Low",
    "Medium",
    "High"
}


# ==========================================
# COMPLAINT CLASSIFICATION
# ==========================================

def classify_complaint(message: str):

    text = message.lower()

    # Payment
    if (
        "payment" in text
        or "paid" in text
        or "money deducted" in text
        or "charged" in text
    ):
        category = "Payment"

    # Refund
    elif (
        "refund" in text
        or "money back" in text
        or "cancelled" in text
    ):
        category = "Refund"

    # Delivery
    elif (
        "delivery" in text
        or "late" in text
        or "delayed" in text
        or "driver" in text
    ):
        category = "Delivery"

    # Technical
    elif (
        "website" in text
        or "app" in text
        or "error" in text
        or "not working" in text
    ):
        category = "Technical"

    # Order
    elif (
        "order" in text
        or "food" in text
        or "item" in text
    ):
        category = "Order"

    else:
        category = "Order"


    # ======================================
    # PRIORITY
    # ======================================

    high_urgency_words = [
        "money deducted",
        "charged but",
        "payment failed",
        "payment deducted",
        "urgent",
        "fraud",
        "wrong charge"
    ]

    if any(word in text for word in high_urgency_words):
        priority = "High"

    elif (
        "late" in text
        or "delayed" in text
        or "refund" in text
    ):
        priority = "Medium"

    else:
        priority = "Low"


    return {
        "category": category,
        "priority": priority
    }


# ==========================================
# COMPLAINT AUTOMATION
# ==========================================

def process_complaint(
    customer_id: str,
    message: str
):

    classification = classify_complaint(message)

    category = classification["category"]
    priority = classification["priority"]


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if category not in ALLOWED_CATEGORIES:
        return {
            "success": False,
            "error": "INVALID_CATEGORY"
        }

    if priority not in ALLOWED_PRIORITIES:
        return {
            "success": False,
            "error": "INVALID_PRIORITY"
        }


    # --------------------------------------
    # CREATE SUPPORT TICKET
    # --------------------------------------

    ticket_result = create_support_ticket(
        customer_id=customer_id,
        category=category,
        priority=priority,
        description=message
    )


    # --------------------------------------
    # RETURN AUTOMATION RESULT
    # --------------------------------------

    return {
        "success": ticket_result.get("success", False),
        "classification": classification,
        "ticket": ticket_result.get("ticket"),
        "error": ticket_result.get("error")
    }