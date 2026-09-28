import json
from pathlib import Path


ORDERS_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


def get_order_status(order_id: str):
    """
    Retrieve the current status of an order.
    """

    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            orders = json.load(file)

        for order in orders:
            if order["order_id"] == order_id:
                return {
                    "success": True,
                    "order_id": order_id,
                    "status": order["status"],
                    "estimated_delivery": order["estimated_delivery"]
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
            "message": "Unable to retrieve order status",
            "details": str(e)
        }