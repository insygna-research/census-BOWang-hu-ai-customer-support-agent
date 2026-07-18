"""
AI 瀹㈡湇鑱婂ぉ鏈哄櫒浜��� - FastAPI 涓诲叆鍙���
鎻愪緵 RESTful API 鎺ュ彛
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app import settings
from app.agent import chat

# 閰嶇疆鏃ュ織
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ===== 鏁版嵁妯″瀷 =====

class ChatRequest(BaseModel):
    """鑱婂ぉ璇锋眰"""
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    """鑱婂ぉ鍝嶅簲"""
    reply: str
    session_id: str
    success: bool
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """鍋ュ悍妫���鏌ュ搷搴���"""
    status: str
    api_key_configured: bool
    version: str = "1.0.0"


# ===== 搴旂敤鐢熷懡鍛ㄦ湡 =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    """搴旂敤鐢熷懡鍛ㄦ湡绠＄悊"""
    logger.info("馃殌 AI 瀹㈡湇鑱婂ぉ鏈哄櫒浜哄惎鍔ㄤ腑...")
    if not settings.is_api_key_set:
        logger.warning("鈿狅笍  OPENAI_API_KEY 鏈���閰嶇疆锛佽���峰湪 .env 鏂囦欢涓���璁剧疆銆���")
    yield
    logger.info("馃憢 AI 瀹㈡湇鑱婂ぉ鏈哄櫒浜哄凡鍏抽棴銆���")


# ===== 鍒涘缓搴旂敤 =====

app = FastAPI(
    title="AI 瀹㈡湇鑱婂ぉ鏈哄櫒浜��� API",
    description="鍩轰簬 LangChain 鐨勬櫤鑳藉���㈡湇浠ｇ悊锛屾敮鎸佽���㈠崟鏌ヨ������銆侀������鎹㈣揣鏀跨瓥銆丗AQ 绛���",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 閰嶇疆
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== API 璺���鐢��� =====

@app.get("/health", response_model=HealthResponse, tags=["绯荤粺"])
async def health_check():
    """鍋ュ悍妫���鏌ョ������鐐���"""
    return HealthResponse(
        status="ok",
        api_key_configured=settings.is_api_key_set,
    )


@app.post("/chat", response_model=ChatResponse, tags=["鑱婂ぉ"])
async def chat_endpoint(request: ChatRequest):
    """澶勭悊鐢ㄦ埛鑱婂ぉ娑堟伅"""
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="娑堟伅涓嶈兘涓虹┖")

    logger.info(f"鏀跺埌娑堟伅 [浼氳瘽:{request.session_id}]: {request.message[:50]}...")
    result = await chat(request.message, request.session_id)
    return ChatResponse(**result)


@app.post("/chat/stream", tags=["鑱婂ぉ"])
async def chat_stream_endpoint(request: ChatRequest):
    """娴佸紡鑱婂ぉ锛堥���勭暀 - 瀹為檯椤圭洰涓���鍙���鐢��� SSE锛���"""
    # 绠���鍖栫増鏈���锛岀洿鎺ヨ繑鍥為潪娴佸紡缁撴灉
    result = await chat(request.message, request.session_id)
    return ChatResponse(**result)


# ===== 鐩存帴杩愯������ =====

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )
