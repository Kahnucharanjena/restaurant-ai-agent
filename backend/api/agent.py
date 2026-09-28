from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.agent.orchestrator import process_message


router = APIRouter(
    prefix="/api/agent",
    tags=["Agent"]
)


# ==========================================
# REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):

    session_id: str = Field(
        ...,
        min_length=1
    )

    customer_id: str = Field(
        ...,
        min_length=1
    )

    message: str = Field(
        ...,
        min_length=1
    )


# ==========================================
# CHAT ENDPOINT
# ==========================================

@router.post("/chat")
def chat(request: ChatRequest):

    return process_message(
        session_id=request.session_id,
        customer_id=request.customer_id,
        message=request.message
    )