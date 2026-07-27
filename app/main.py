"""
AI Customer Support Agent - FastAPI Main Entry

Provides RESTful API endpoints for the customer service agent.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import settings
from app.agent import chat, reset_agent

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ===== Data Models =====


class ChatRequest(BaseModel):
    """Chat request payload."""
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    """Chat response payload."""
    reply: str
    session_id: str
    success: bool
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    api_key_configured: bool
    version: str = "1.0.0"


# ===== Application Lifecycle =====


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management."""
    logger.info("🚀 AI Customer Support Agent starting up...")
    if not settings.is_api_key_set:
        logger.warning("⚠️  OPENAI_API_KEY not configured! Set it in .env file.")
    yield
    logger.info("👋 AI Customer Support Agent shutting down.")


# ===== Create Application =====

app = FastAPI(
    title="AI Customer Support Agent API",
    description="Intelligent customer service agent powered by LangChain. Supports order inquiries, return policies, FAQ, and more.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== API Routes =====


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="ok",
        api_key_configured=settings.is_api_key_set,
    )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_endpoint(request: ChatRequest):
    """Process a chat message from the user."""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    logger.info(f"Received message [session:{request.session_id}]: {request.message[:50]}...")
    result = await chat(request.message, request.session_id)
    return ChatResponse(**result)


@app.post("/reset", tags=["System"])
async def reset_agent_endpoint():
    """Reset the agent instance (clears memory and reinitializes)."""
    reset_agent()
    return {"message": "Agent reset successfully"}


# ===== Direct Execution =====

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )
