"""
AI 瀹㈡湇鑱婂ぉ鏈哄櫒浜��� - Streamlit 鐢ㄦ埛鐣岄潰
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st
import requests

# 娣诲姞椤圭洰鏍圭洰褰曞埌 path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import settings

# ===== 椤甸潰閰嶇疆 =====
st.set_page_config(
    page_title="AI 鏅鸿兘瀹㈡湇",
    page_icon="馃������",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== 鏍峰紡 =====
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


# ===== 渚ц竟鏍��� =====
with st.sidebar:
    st.title("馃������ AI 鏅鸿兘瀹㈡湇")
    st.markdown("---")

    # API 閰嶇疆鐘舵������
    api_ok = settings.is_api_key_set
    if api_ok:
        st.success("鉁��� API 宸查厤缃���")
    else:
        st.warning("鈿狅笍 鏈���閰嶇疆 API Key")
        st.info("璇峰垱寤��� .env 鏂囦欢骞惰���剧疆 OPENAI_API_KEY")

    st.markdown("### 鍏充簬")
    st.markdown("""
    鍩轰簬 LangChain 鏋勫缓鐨��� AI 瀹㈡湇浠ｇ悊锛屾敮鎸侊細
    - 馃摝 璁㈠崟鏌ヨ������
    - 馃攧 閫���鎹㈣揣鏀跨瓥
    - 鉂��� 甯歌���侀棶棰���
    - 馃幆 鍏朵粬鍜ㄨ���㈡湇鍔���
    """)

    st.markdown("### 蹇���閫熸彁闂���")
    quick_questions = [
        "鏌ヤ竴涓嬭���㈠崟 ORD-2024-001 鐨勭姸鎬���",
        "浣犱滑鐨勯������鎹㈣揣鏀跨瓥鏄���浠���涔堬紵",
        "浠���涔堟椂鍊欏彂璐э紵",
        "鐜板湪鍑犵偣浜嗭紵",
    ]
    for q in quick_questions:
        if st.button(q, use_container_width=True):
            st.session_state.pending_question = q

    st.markdown("---")
    if st.button("馃棏锔��� 娓呯┖瀵硅瘽", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ===== 涓昏亰澶╃晫闈��� =====

# 鍒濆���嬪寲浼氳瘽鐘舵������
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "浣犲ソ锛佹垜鏄���鏅鸿兘瀹㈡湇灏忔櫤 馃���朶n\n璇烽棶鏈変粈涔堝彲浠ュ府鍔╀綘鐨勶紵浣犲彲浠ユ煡璇㈣���㈠崟銆佷簡瑙ｉ������鎹㈣揣鏀跨瓥銆佸挩璇㈠父瑙侀棶棰樼瓑銆���"}
    ]

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())[:8]

# API 鍩虹������ URL
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


# 鏄剧ず鑱婂ぉ鍘嗗彶
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "human":
            st.markdown(
                f'<div class="chat-message-human">馃檪 {msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="chat-message-ai">馃������ {msg["content"]}</div>',
                unsafe_allow_html=True,
            )


# 澶勭悊寰呭���勭悊闂���棰���
if st.session_state.pending_question:
    question = st.session_state.pending_question
    st.session_state.pending_question = None
    # 鐩存帴鍙戦������
    st.session_state.messages.append({"role": "human", "content": question})

    with st.spinner("灏忔櫤姝ｅ湪鎬濊������..."):
        try:
            response = requests.post(
                f"{API_BASE}/chat",
                json={"message": question, "session_id": st.session_state.session_id},
                timeout=30,
            )
            if response.status_code == 200:
                reply = response.json()["reply"]
                st.session_state.messages.append({"role": "ai", "content": reply})
            else:
                st.session_state.messages.append({
                    "role": "ai",
                    "content": f"馃槄 鎶辨瓑锛岃���锋眰鍑洪敊浜嗭細{response.text}"
                })
        except requests.exceptions.ConnectionError:
            st.session_state.messages.append({
                "role": "ai",
                "content": "馃槄 鏃犳硶杩炴帴鍒��� API 鏈嶅姟鍣���锛岃���风‘璁ゅ悗绔���宸插惎鍔ㄣ���俓n\n杩愯���屽懡浠わ細`uvicorn app.main:app --reload`"
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "ai",
                "content": f"馃槄 鍑洪敊浜嗭細{str(e)}"
            })
    st.rerun()


# 鐢ㄦ埛杈撳叆
st.markdown("---")
with st.container():
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "杈撳叆浣犵殑闂���棰���...",
            key="user_input",
            placeholder="渚嬪���傦細鏌ヤ竴涓嬫垜鐨勮���㈠崟鐘舵������",
            label_visibility="collapsed",
        )
    with col2:
        send = st.button("鍙戦������ 馃摛", use_container_width=True)

    if send and user_input:
        st.session_state.messages.append({"role": "human", "content": user_input})

        with st.spinner("灏忔櫤姝ｅ湪鎬濊������..."):
            try:
                response = requests.post(
                    f"{API_BASE}/chat",
                    json={"message": user_input, "session_id": st.session_state.session_id},
                    timeout=30,
                )
                if response.status_code == 200:
                    reply = response.json()["reply"]
                    st.session_state.messages.append({"role": "ai", "content": reply})
                else:
                    st.session_state.messages.append({
                        "role": "ai",
                        "content": f"馃槄 鎶辨瓑锛岃���锋眰鍑洪敊浜嗭細{response.text}"
                    })
            except requests.exceptions.ConnectionError:
                st.session_state.messages.append({
                    "role": "ai",
                    "content": "馃槄 鏃犳硶杩炴帴鍒��� API 鏈嶅姟鍣���锛岃���风‘璁ゅ悗绔���宸插惎鍔ㄣ���俓n\n杩愯���屽懡浠わ細`uvicorn app.main:app --reload`"
                })
            except Exception as e:
                st.session_state.messages.append({
                    "role": "ai",
                    "content": f"馃槄 鍑洪敊浜嗭細{str(e)}"
                })
        st.rerun()

# 搴曢儴鎻愮ず
st.markdown("---")
st.caption("馃挕 鎻愮ず锛氳緭鍏ヤ换鎰忛棶棰樺紑濮嬪���硅瘽锛屾垨鐐瑰嚮宸︿晶蹇���鎹烽棶棰���")
