import json
from pathlib import Path


ORDERS_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


def get_order_details(order_id: str):
    """
    Retrieve complete details of an order.
    """

    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            orders = json.load(file)

        for order in orders:
            if order["order_id"] == order_id:
                return {
                    "success": True,
                    "order": order
                }

        return {
            "success": False,
            "error": "ORDER_NOT_FOUND",
            "message": f"No order found with ID {order_id}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": "ORDER_API_ERROR",
            "message": "Unable to retrieve order details",
            "details": str(e)
        }