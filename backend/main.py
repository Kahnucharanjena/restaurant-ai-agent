from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.orders import router as orders_router
from backend.api.tickets import router as tickets_router
from backend.api.agent import router as agent_router

app = FastAPI(
    title="Restaurant AI Support Agent",
    description="AI-powered restaurant support and operations agent",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(orders_router)
app.include_router(tickets_router)
app.include_router(agent_router)

@app.get("/")
def root():
    return {
        "message": "Restaurant AI Support Agent is running",
        "status": "online"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }