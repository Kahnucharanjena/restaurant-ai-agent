from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.tools.support_ticket import create_support_ticket


router = APIRouter(
    prefix="/api/support",
    tags=["Support"]
)


class SupportTicketRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    priority: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)


@router.post("/tickets")
def create_ticket(request: SupportTicketRequest):

    return create_support_ticket(
        customer_id=request.customer_id,
        category=request.category,
        priority=request.priority,
        description=request.description
    )