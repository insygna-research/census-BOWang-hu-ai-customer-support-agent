# AI ç€¹ãˆ¡æ¹‡é‘±å©‚ã‰éˆå“„æ«’æµœí²º - Dockerfile

# ===== é‹å‹«ç¼“é—ƒèˆµí²®í²µ =====
FROM python:3.12-slim AS builder

WORKDIR /app

# ç€¹å¤í²£å‘¯éƒ´ç¼ç†¶ç··ç’§í²–
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# æ¾¶å¶…åŸ—æ¸šæ¿Šç¦†é‚å›¦æ¬¢éªè·ºç•¨ç‘í²…
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ===== æ©æ„¯í²¡å²„æ¨å¨ˆí²µ =====
FROM python:3.12-slim

WORKDIR /app

# æµ åº¢ç€¯å¯¤æ´ªæ¨å¨ˆé›í²¤å¶…åŸ—å®¸æ’ç•¨ç‘å‘¯æ®‘é–í²…
COPY --from=builder /root/.local /root/.local

# çº­í²®æ·‡æ¿‡æ¹°é¦í²° bin é¦í²¨ PATH æ¶“í²­
ENV PATH=/root/.local/bin:$PATH

# æ¾¶å¶…åŸ—æ´æ—‚æ•¤æµ ï½‡çˆœ
COPY . .

# é’æ¶˜ç¼“é­ãƒ¨ç˜‘æ´æ’¶æ´°è¤°í²•
RUN mkdir -p knowledge_base

# é†æ’®æ¹¶ç»”í²¯é™í²£
EXPOSE 8000 8501

# é‹ãƒ¥æ‚å¦«í²€éŒí²¥
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# æ¦›æ¨¿í²®ã‚…æƒé”í²¨ API éˆå¶…å§Ÿ
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
