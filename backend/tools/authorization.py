import json
from pathlib import Path


# ============================================================
# ORDERS DATA FILE
# ============================================================

ORDERS_FILE = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "orders.json"
)


# ============================================================
# ORDER AUTHORIZATION
# ============================================================

def check_order_authorization(
    customer_id: str,
    order_id: str
):
    """
    Check whether a customer is authorized
    to access a particular order.
    """

    # --------------------------------------------------------
    # Validate customer ID
    # --------------------------------------------------------

    if not customer_id or not customer_id.strip():

        return {
            "authorized": False,
            "error": "INVALID_CUSTOMER_ID",
            "message": "Customer ID is required."
        }


    # --------------------------------------------------------
    # Validate order ID
    # --------------------------------------------------------

    if not order_id or not order_id.strip():

        return {
            "authorized": False,
            "error": "INVALID_ORDER_ID",
            "message": "Order ID is required."
        }


    customer_id = customer_id.strip().upper()
    order_id = order_id.strip().upper()


    # --------------------------------------------------------
    # Read orders database
    # --------------------------------------------------------

    try:

        with open(
            ORDERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            orders = json.load(file)

    except FileNotFoundError:

        return {
            "authorized": False,
            "error": "ORDERS_FILE_NOT_FOUND",
            "message": "Order data is unavailable."
        }

    except json.JSONDecodeError:

        return {
            "authorized": False,
            "error": "INVALID_ORDER_DATA",
            "message": "Order data is invalid."
        }

    except Exception as error:

        return {
            "authorized": False,
            "error": "AUTHORIZATION_ERROR",
            "message": "Unable to verify order authorization.",
            "details": str(error)
        }


    # --------------------------------------------------------
    # Find requested order
    # --------------------------------------------------------

    for order in orders:

        current_order_id = str(
            order.get("order_id", "")
        ).upper()


        if current_order_id == order_id:

            order_customer_id = str(
                order.get("customer_id", "")
            ).upper()


            # ------------------------------------------------
            # AUTHORIZED
            # ------------------------------------------------

            if order_customer_id == customer_id:

                return {
                    "authorized": True,
                    "customer_id": customer_id,
                    "order_id": order_id,
                    "message": (
                        "Customer is authorized to access this order."
                    )
                }


            # ------------------------------------------------
            # UNAUTHORIZED
            # ------------------------------------------------

            return {
                "authorized": False,
                "error": "UNAUTHORIZED_ORDER_ACCESS",
                "customer_id": customer_id,
                "order_id": order_id,
                "message": (
                    "This order does not belong "
                    "to the authenticated customer."
                )
            }


    # --------------------------------------------------------
    # ORDER NOT FOUND
    # --------------------------------------------------------

    return {
        "authorized": False,
        "error": "ORDER_NOT_FOUND",
        "customer_id": customer_id,
        "order_id": order_id,
        "message": "Order was not found."
    }