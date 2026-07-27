# AI Customer Support Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/LangChain-0.3-green" alt="LangChain">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-brightgreen" alt="OpenAI">
  <img src="https://img.shields.io/badge/FastAPI-0.115-teal?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-1.43-red?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
</p>

An intelligent customer service chatbot built with **LangChain + OpenAI**, providing automated order inquiries, return/exchange policy consultations, FAQ answers, and more.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📦 **Order Tracking** | Look up order status, shipping info, and estimated delivery |
| 🔄 **Return/Exchange Policy** | Automated answers about returns, refunds, and after-sales |
| 💬 **FAQ Matching** | Smart keyword matching for frequently asked questions |
| 🧠 **Conversation Memory** | Long conversation memory via `ConversationSummaryBufferMemory` |
| 🖥️ **Web UI** | Friendly chat interface built with Streamlit |
| 🔌 **REST API** | Standard HTTP API via FastAPI |
| 🐳 **Docker Support** | One-click containerized deployment |

## 🏗️ Architecture

```
User Input → Streamlit UI → FastAPI → LangChain Agent → OpenAI LLM
                                    ↓
                              Tools Layer
                    ┌──────────┬──────────┬──────────┬──────────┐
                    │  Order   │ Return   │   FAQ    │  Time    │
                    └──────────┴──────────┴──────────┴──────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API Key

### 1️⃣ Local Development

```bash
# Clone the repository
git clone https://github.com/BOWang-hu/-ai-customer-support-agent.git
cd -ai-customer-support-agent

# Configure environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# Install dependencies
pip install -r requirements.txt

# Start API server
uvicorn app.main:app --reload
# API runs at http://localhost:8000

# Start Web UI (new terminal)
streamlit run app/ui.py
# UI runs at http://localhost:8501
```

### 2️⃣ Docker Deployment

```bash
# Edit .env with your API Key
cp .env.example .env

# One-click start
docker-compose up -d

# Access UI: http://localhost:8501
# API docs: http://localhost:8000/docs
```

### 3️⃣ API Usage Example

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "Check order ORD-2024-001 status", "session_id": "user123"}
)
print(response.json()["reply"])
# Output: Order ORD-2024-001 status: Shipped, ETA: 2024-12-25, Carrier: SF Express
```

## 📁 Project Structure

```
-ai-customer-support-agent/
├── app/
│   ├── __init__.py      # Configuration management
│   ├── main.py          # FastAPI application entry
│   ├── agent.py         # LangChain Agent core logic
│   └── ui.py            # Streamlit user interface
├── knowledge_base/      # Knowledge base files (optional)
├── .env.example         # Environment variable template
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build
├── docker-compose.yml   # Container orchestration
└── README.md            # Project documentation
```

## 🛠️ Technical Highlights

1. **Agent Pattern**: Uses OpenAI Tools Agent — LLM autonomously decides which tools to invoke
2. **Conversation Memory**: `ConversationSummaryBufferMemory` auto-summarizes long conversations, controlling token consumption
3. **Tool Encapsulation**: Each customer service function is an independent Tool, easy to extend
4. **Graceful Degradation**: Multi-layer exception handling; auto-switches to mock mode when API Key is missing
5. **Session Management**: Supports multi-user sessions with independent conversation histories

## 🚀 Related AI Projects

Check out my other AI agent projects:

| Project | Description |
|---------|-------------|
| [AI Multi-Agent Workflow](https://github.com/BOWang-hu/ai-multi-agent-workflow) | Multi-agent collaboration system with Researcher, Writer, Reviewer & Coordinator roles |
| [AI RAG Knowledge Agent](https://github.com/BOWang-hu/ai-rag-knowledge-agent) | Document Q&A using RAG with Chroma vector database |
| [AI Code Review Agent](https://github.com/BOWang-hu/ai-code-review-agent) | Automated code review combining static analysis with AI |

---

## 📄 License

MIT — feel free to use, modify, and distribute.
