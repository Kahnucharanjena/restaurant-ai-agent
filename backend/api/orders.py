from fastapi import APIRouter

from backend.tools.order_status import get_order_status
from backend.tools.order_details import get_order_details


router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)


@router.get("/{order_id}/status")
def order_status(order_id: str):
    return get_order_status(order_id)


@router.get("/{order_id}")
def order_details(order_id: str):
    return get_order_details(order_id)