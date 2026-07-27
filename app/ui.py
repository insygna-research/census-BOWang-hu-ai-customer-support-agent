"""
AI Customer Support Agent - Streamlit User Interface

Provides a friendly chat interface for the customer service agent.
"""
from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

import streamlit as st
import requests

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import settings

# ===== Page Configuration =====
st.set_page_config(
    page_title="AI Smart Customer Service",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== Custom Styles =====
st.markdown("""
<style>
    .chat-message-human {
        background-color: #e3f2fd;
        border-radius: 15px 15px 5px 15px;
        padding: 12px 18px;
        margin: 8px 0;
        text-align: right;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .chat-message-ai {
        background-color: #f5f5f5;
        border-radius: 15px 15px 15px 5px;
        padding: 12px 18px;
        margin: 8px 0;
        max-width: 80%;
        float: left;
        clear: both;
    }
    .chat-container {
        overflow-y: auto;
        padding: 10px;
        background: white;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# API base URL
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


# ===== Session State Initialization =====
def init_session_state():
    """Initialize all session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "ai",
                "content": (
                    "Hello! I'm your AI Customer Service Assistant 🎯\n\n"
                    "I can help you with:\n"
                    "- 📦 Order status inquiries\n"
                    "- 🔄 Return/exchange policies\n"
                    "- ❓ FAQ answers\n"
                    "- ⏰ Time queries\n\n"
                    "How can I help you today?"
                ),
            }
        ]

    if "pending_question" not in st.session_state:
        st.session_state.pending_question = None

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]


init_session_state()


# ===== Sidebar =====
with st.sidebar:
    st.title("🎯 AI Customer Service")
    st.markdown("---")

    # API configuration status
    api_ok = settings.is_api_key_set
    if api_ok:
        st.success("✅ API Configured")
    else:
        st.warning("⚠️ API Key not set")
        st.info("Create a `.env` file and set `OPENAI_API_KEY`")

    st.markdown("### About")
    st.markdown("""
    AI customer service agent built with LangChain.
    - 📦 Order tracking
    - 🔄 Return policy
    - ❓ FAQ
    - 🎯 Other services
    """)

    st.markdown("### Quick Questions")
    quick_questions = [
        "Check order ORD-2024-001 status",
        "What's your return policy?",
        "When do you ship?",
        "What time is it now?",
    ]
    for q in quick_questions:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())[:8]
        st.rerun()

    # Session ID display
    st.caption(f"Session: {st.session_state.session_id}")


# ===== Main Chat Interface =====

# Display chat history
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "human":
            st.markdown(
                f'<div class="chat-message-human">👤 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-message-ai">🤖 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )


def send_message(message: str):
    """Send a message to the API and update the chat."""
    st.session_state.messages.append({"role": "human", "content": message})

    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"message": message, "session_id": st.session_state.session_id},
                timeout=30,
            )
            if response.status_code == 200:
                reply = response.json()["reply"]
                st.session_state.messages.append({"role": "ai", "content": reply})
            else:
                st.session_state.messages.append({
                    "role": "ai",
                    "content": f"😅 Sorry, request failed: {response.text}"
                })
        except requests.exceptions.ConnectionError:
            st.session_state.messages.append({
                "role": "ai",
                "content": (
                    "😅 Cannot connect to the API server. "
                    "Please make sure the backend is running.\n\n"
                    "Run: `uvicorn app.main:app --reload`"
                )
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "ai",
                "content": f"😅 Error: {str(e)}"
            })


# Handle pending question
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
    send_message(question)
    st.rerun()

# User input
st.markdown("---")
with st.container():
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "Type your message...",
            key="user_input",
            placeholder="e.g., Check my order status",
            label_visibility="collapsed",
        )
    with col2:
        send = st.button("Send 📤", use_container_width=True)

    if send and user_input:
        send_message(user_input)
        st.rerun()

# Footer
st.markdown("---")
st.caption("💡 Type a question to start chatting, or click a quick question on the left")
