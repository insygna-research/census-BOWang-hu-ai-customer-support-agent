"""
AI 瀹㈡湇鑱婂ぉ鏈哄櫒浜��� - 鏍稿績閰嶇疆妯″潡
"""
from __future__ import annotations

import os
from pathlib import Path
from dataclasses import dataclass, field

from dotenv import load_dotenv

# 鍔犺浇 .env 鏂囦欢
load_dotenv()


@dataclass
class Settings:
    """搴旂敤閰嶇疆"""

    # OpenAI
    openai_api_key: str = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", "")
    )
    openai_base_url: str = field(
        default_factory=lambda: os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    )
    openai_model_name: str = field(
        default_factory=lambda: os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    )

    # 搴旂敤
    app_host: str = field(default_factory=lambda: os.getenv("APP_HOST", "0.0.0.0"))
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # 鐭ヨ瘑搴���
    knowledge_base_path: str = field(
        default_factory=lambda: os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_base")
    )

    # Chroma 鎸佷箙鍖栫洰褰���
    chroma_persist_dir: str = "./chroma_db"

    @property
    def is_api_key_set(self) -> bool:
        return bool(self.openai_api_key) and self.openai_api_key != "sk-your-api-key-here"


# 鍏ㄥ眬鍗曚緥
settings = Settings()
