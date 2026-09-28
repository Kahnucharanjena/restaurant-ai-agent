# ==========================================
# TOOL SCHEMAS FOR THE AI AGENT
# ==========================================

TOOL_SCHEMAS = [
    {
        "name": "get_order_status",
        "description": (
            "Get the current status and estimated delivery time "
            "for a specific customer order. Use this when the "
            "customer asks where an order is or asks for its status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The customer's order ID, for example ORD-1005."
                }
            },
            "required": ["order_id"]
        }
    },

    {
        "name": "get_order_details",
        "description": (
            "Get the complete details of a specific customer order, "
            "including restaurant, items, payment status and order status."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The customer's order ID."
                }
            },
            "required": ["order_id"]
        }
    },

    {
        "name": "create_support_ticket",
        "description": (
            "Create a support ticket when a customer has an unresolved "
            "support issue that requires escalation. The application "
            "must validate authorization and ticket information before "
            "creating the ticket."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Authenticated customer ID."
                },
                "category": {
                    "type": "string",
                    "enum": [
                        "Payment",
                        "Order",
                        "Delivery",
                        "Refund",
                        "Technical"
                    ],
                    "description": "Support issue category."
                },
                "priority": {
                    "type": "string",
                    "enum": [
                        "Low",
                        "Medium",
                        "High"
                    ],
                    "description": "Support priority."
                },
                "description": {
                    "type": "string",
                    "description": "Clear description of the customer's issue."
                }
            },
            "required": [
                "customer_id",
                "category",
                "priority",
                "description"
            ]
        }
    },

    {
        "name": "search_knowledge_base",
        "description": (
            "Search the restaurant knowledge base for documented "
            "policies, FAQs, cancellation rules, refund information, "
            "delivery information and support procedures. Use this "
            "instead of inventing policy information."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The question or topic to search for."
                }
            },
            "required": ["query"]
        }
    }
]