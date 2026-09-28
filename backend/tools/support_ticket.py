import json
from pathlib import Path


TICKETS_FILE = Path(__file__).resolve().parent.parent / "data" / "tickets.json"


def create_support_ticket(
    customer_id: str,
    category: str,
    priority: str,
    description: str
):
    """
    Create a new customer support ticket.
    """

    try:
        # Load existing tickets
        with open(TICKETS_FILE, "r", encoding="utf-8") as file:
            tickets = json.load(file)

        # Generate ticket ID
        ticket_number = len(tickets) + 1
        ticket_id = f"TKT-{ticket_number:04d}"

        # Create ticket
        ticket = {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "category": category,
            "priority": priority,
            "description": description,
            "status": "Open"
        }

        # Add ticket
        tickets.append(ticket)

        # Save tickets
        with open(TICKETS_FILE, "w", encoding="utf-8") as file:
            json.dump(tickets, file, indent=4)

        return {
            "success": True,
            "ticket": ticket
        }

    except Exception as e:
        return {
            "success": False,
            "error": "TICKET_CREATION_ERROR",
            "message": "Unable to create support ticket",
            "details": str(e)
        }