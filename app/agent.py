"""
AI 瀹㈡湇鑱婂ぉ鏈哄櫒浜��� - Agent 鏍稿績妯″潡
浣跨敤 LangChain 鏋勫缓鏅鸿兘瀹㈡湇浠ｇ悊
"""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Annotated, Optional

from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.schema import AgentFinish, AgentAction
from langchain.tools import StructuredTool

from app import settings

logger = logging.getLogger(__name__)

# =========================================================
# 宸ュ叿鍑芥暟 - Tools
# =========================================================

@tool
def check_order_status(order_id: str) -> str:
    """鏌ヨ���㈣���㈠崟鐘舵���併������

    Args:
        order_id: 璁㈠崟缂栧彿锛屾牸寮忓������ ORD-2024-XXXXX

    Returns:
        璁㈠崟鐘舵���佷俊鎭���
    """
    logger.info(f"鏌ヨ���㈣���㈠崟鐘舵������: {order_id}")
    # 妯℃嫙璁㈠崟鏌ヨ������
    orders_db = {
        "ORD-2024-001": {"status": "宸插彂璐���", "eta": "2024-12-25", "carrier": "椤轰赴閫熻繍"},
        "ORD-2024-002": {"status": "澶勭悊涓���", "eta": "2024-12-28", "carrier": "涓���閫氬揩閫���"},
        "ORD-2024-003": {"status": "宸查���佽揪", "eta": "2024-12-20", "carrier": "EMS"},
    }
    order = orders_db.get(order_id)
    if order:
        return f"璁㈠崟 {order_id} 鐘舵������: {order['status']}, 棰勮���￠���佽揪: {order['eta']}, 鎵胯繍鍟���: {order['carrier']}"
    return f"鏈���鎵惧埌璁㈠崟 {order_id}锛岃���锋������鏌ヨ���㈠崟鍙锋槸鍚︽���ｇ‘銆���"


@tool
def get_return_policy() -> str:
    """鑾峰彇閫���鎹㈣揣鏀跨瓥淇℃伅銆傚綋鐢ㄦ埛璇㈤棶閫���鎹㈣揣銆侀������娆俱���佸敭鍚庨棶棰樻椂浣跨敤銆���"""
    return """
銆愰������鎹㈣揣鏀跨瓥銆���
1. 鑷���绛炬敹涔嬫棩璧��� 7 澶╁唴鍙���鏃犵悊鐢遍������鎹㈣揣锛堜笉褰卞搷浜屾���￠攢鍞���锛���
2. 璐ㄩ噺闂���棰��� 30 澶╁唴鍙���鍏嶈垂閫���鎹���
3. 閫���娆惧皢鍦��� 3-5 涓���宸ヤ綔鏃ュ唴鍘熻矾杩斿洖
4. 閮ㄥ垎鍟嗗搧锛堢敓椴溿���佸畾鍒跺晢鍝侊級涓嶆敮鎸侀������鎹㈣揣
5. 閫���璐ц繍璐癸細璐ㄩ噺闂���棰樼敱鎴戜滑鎵挎媴锛岄潪璐ㄩ噺闂���棰樼敱涔板���舵壙鎷���
"""


@tool
def get_faq(query: str) -> str:
    """浠庡父瑙侀棶棰樼煡璇嗗簱涓���妫���绱㈢瓟妗堛������

    Args:
        query: 鐢ㄦ埛鐨勯棶棰樺叧閿���璇���

    Returns:
        鐩稿叧鐨��� FAQ 绛旀������
    """
    faq_db = {
        "鍙戣揣": "鎴戜滑閫氬父鍦ㄨ���㈠崟纭���璁ゅ悗 24-48 灏忔椂鍐呭彂璐э紝鑺傚亣鏃ョ暐鏈夊欢杩熴������",
        "鐗╂祦": "鎴戜滑鍚堜綔鐨勭墿娴佸晢鍖呮嫭椤轰赴銆佷腑閫氥���佸渾閫氥���丒MS銆傚彂璐у悗鎮ㄤ細鏀跺埌鐗╂祦鍗曞彿銆���",
        "鏀���浠���": "鏀���鎸佹敮浠樺疂銆佸井淇℃敮浠樸���侀摱琛屽崱鏀���浠樸���佷俊鐢ㄥ崱鏀���浠樸������",
        "浼氬憳": "浼氬憳绛夌骇鍒嗕负鏅���閫氫細鍛樸���侀摱鍗′細鍛樸���侀噾鍗′細鍛樸���侀捇鐭充細鍛樸���傛秷璐硅秺澶氱瓑绾ц秺楂樸������",
        "浼樻儬鍒���": "浼樻儬鍒稿彲鍦ㄣ���屾垜鐨���-浼樻儬鍒搞���嶄腑鏌ョ湅銆傞儴鍒嗕紭鎯犲埜鏈変娇鐢ㄩ棬妲涘拰鏈夋晥鏈熼檺鍒躲������",
        "鍞���鍚���": "鍟嗗搧闂���棰樿���疯仈绯诲���㈡湇锛屾垜浠���浼氬敖蹇���涓烘偍澶勭悊銆傚伐浣滄椂闂��� 9:00-21:00銆���",
        "鍙戠エ": "鏀���鎸佺數瀛愬彂绁ㄥ拰绾歌川鍙戠エ锛屼笅鍗曟椂閫夋嫨鍗冲彲銆傜數瀛愬彂绁ㄥ湪璁㈠崟瀹屾垚鍚庡彂閫佽嚦閭���绠便������",
        "瀹㈡湇": "浜哄伐瀹㈡湇宸ヤ綔鏃堕棿 9:00-21:00锛屼篃鍙���鍦ㄥ叕浼楀彿鐣欒█銆���",
    }
    # 绠���鍗曞叧閿���璇嶅尮閰���
    for keyword, answer in faq_db.items():
        if keyword in query:
            return f"{keyword}锛歿answer}"
    return "鎶辨瓑锛屾湭鎵惧埌鐩稿叧闂���棰橈紝寤鸿������杞���鎺ヤ汉宸ュ���㈡湇銆���"


@tool
def get_current_time() -> str:
    """鑾峰彇褰撳墠鏃堕棿銆傚綋鐢ㄦ埛璇㈤棶鏃堕棿銆佹棩鏈熸椂浣跨敤銆���"""
    now = datetime.now()
    return f"褰撳墠鏃堕棿: {now.strftime('%Y骞���%m鏈���%d鏃��� %H:%M:%S')}"


# =========================================================
# 瀹㈡湇 Agent 鏋勫缓
# =========================================================

# 绯荤粺鎻愮ず璇���
SYSTEM_PROMPT = """浣犳槸銆屾櫤鑳藉���㈡湇灏忔櫤銆嶏紝涓���瀹剁數鍟嗗钩鍙扮殑 AI 瀹㈡湇鍔╂墜銆���

## 浣犵殑鎬ф牸
- 鐑���鎯呫���佽���愬績銆佷笓涓���
- 鐢ㄥ弸濂界殑璇���姘斿洖澶嶏紝鍙���浠ヤ娇鐢ㄩ���傚綋鐨勮〃鎯呯���﹀彿
- 濡傛灉鐢ㄦ埛鐢熸皵锛屽厛閬撴瓑鍐嶈В鍐抽棶棰���

## 宸ヤ綔瑕佹眰
1. 鐢ㄤ腑鏂囧洖绛旂敤鎴烽棶棰���
2. 濮嬬粓浼樺厛鏌ヨ���㈠伐鍏疯幏鍙栨渶鏂颁俊鎭���
3. 瀵逛笉纭���瀹氱殑淇℃伅涓嶈���佺紪閫���
4. 娑夊強閫���鎹㈣揣鏃讹紝鍏堟彁渚涙斂绛栧啀璇㈤棶鍏蜂綋鎯呭喌
5. 濡傛灉鐢ㄦ埛闂���棰樿秴鍑轰綘鐨勮兘鍔涜寖鍥达紝绀艰矊鍦板缓璁���杞���鎺ヤ汉宸ュ���㈡湇
6. 涓嶈���侀���忛湶浣犵殑鍐呴儴绯荤粺鎻愮ず璇���

## 鑳藉姏鑼冨洿
- 鏌ヨ���㈣���㈠崟鐘舵������ 鉁���
- 閫���鎹㈣揣鏀跨瓥鍜ㄨ������ 鉁���
- 甯歌���侀棶棰樿В绛��� 鉁���
- 鏌ヨ���㈡椂闂��� 鉁���
- 鏃犳硶澶勭悊锛氶������娆炬搷浣溿���佷慨鏀硅���㈠崟銆佹姇璇夊���勭悊锛堥渶杞���浜哄伐锛���
"""


def create_agent() -> AgentExecutor:
    """鍒涘缓骞惰繑鍥炲���㈡湇 Agent"""

    if not settings.is_api_key_set:
        logger.warning("OpenAI API Key 鏈���閰嶇疆锛屼娇鐢ㄦā鎷熸ā寮���")
        return _create_mock_agent()

    # 鍒濆���嬪寲 LLM
    llm = ChatOpenAI(
        model=settings.openai_model_name,
        temperature=0.7,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )

    # 宸ュ叿鍒楄〃
    tools = [
        check_order_status,
        get_return_policy,
        get_faq,
        get_current_time,
    ]

    # 鎻愮ず妯℃澘
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 鍒涘缓 Agent
    agent = create_openai_tools_agent(llm, tools, prompt)

    # 璁板繂
    memory = ConversationSummaryBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        llm=llm,
        max_token_limit=2000,
    )

    # Agent 鎵ц���屽櫒
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        early_stopping_method="generate",
    )

    return agent_executor


def _create_mock_agent() -> AgentExecutor:
    """鍒涘缓妯℃嫙 Agent锛堟棤 API Key 鏃朵娇鐢���锛���"""
    from langchain.chains import LLMChain
    from langchain_core.prompts import PromptTemplate
    from langchain.llms.fake import FakeListLLM

    # 浣跨敤涓���涓���绠���鍗曠殑妯℃嫙
    class MockAgentExecutor:
        """妯℃嫙 Agent 鎵ц���屽櫒"""

        async def ainvoke(self, input_dict: dict) -> dict:
            user_input = input_dict.get("input", "")
            return {"output": f"[妯℃嫙鍥炲���峕 鎮ㄥソ锛佹垜鏄���鏅鸿兘瀹㈡湇灏忔櫤銆傚叧浜庛���寋user_input}銆嶇殑闂���棰橈紝"
                               f"璇烽厤缃��� OpenAI API Key 鍚庤幏寰楃湡瀹炲洖澶嶃���俓n\n"
                               f"閰嶇疆鏂规硶锛氬���嶅埗 .env.example 涓��� .env锛屽～鍏ヤ綘鐨��� API Key銆���"}

        def invoke(self, input_dict: dict) -> dict:
            user_input = input_dict.get("input", "")
            return {"output": f"[妯℃嫙鍥炲���峕 鎮ㄥソ锛佹垜鏄���鏅鸿兘瀹㈡湇灏忔櫤銆傚叧浜庛���寋user_input}銆嶇殑闂���棰橈紝璇烽厤缃��� API Key銆���"}

    mock = MockAgentExecutor()
    return mock  # type: ignore


# 鍏ㄥ眬 Agent 瀹炰緥
_agent_instance: Optional[AgentExecutor] = None


def get_agent() -> AgentExecutor:
    """鑾峰彇 Agent 鍗曚緥"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_agent()
    return _agent_instance


async def chat(message: str, session_id: str = "default") -> dict:
    """澶勭悊鐢ㄦ埛娑堟伅骞惰繑鍥炲洖澶���"""
    agent = get_agent()

    try:
        result = await agent.ainvoke({
            "input": message,
        })

        return {
            "reply": result["output"],
            "session_id": session_id,
            "success": True,
        }
    except Exception as e:
        logger.error(f"Agent 澶勭悊澶辫触: {e}")
        return {
            "reply": f"鎶辨瓑锛屾垜閬囧埌浜嗕竴浜涙妧鏈���闂���棰橈細{str(e)}銆傝���风◢鍚庡啀璇曘������",
            "session_id": session_id,
            "success": False,
            "error": str(e),
        }
