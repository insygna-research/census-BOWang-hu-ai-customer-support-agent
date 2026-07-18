# 馃������ AI 瀹㈡湇鑱婂ぉ鏈哄櫒浜���

鍩轰簬 **LangChain + OpenAI** 鏋勫缓鐨勬櫤鑳藉���㈡湇浠ｇ悊绯荤粺锛屾彁渚涜���㈠崟鏌ヨ������銆侀������鎹㈣揣鍜ㄨ������銆丗AQ 瑙ｇ瓟绛夎嚜鍔ㄥ���㈡湇鑳藉姏銆���

## 鉁��� 鍔熻兘鐗规������

| 鍔熻兘 | 璇存槑 |
|------|------|
| 馃摝 **璁㈠崟鏌ヨ������** | 鏍规嵁璁㈠崟鍙锋煡璇㈢墿娴佺姸鎬併���侀���勮���￠���佽揪鏃堕棿 |
| 馃攧 **閫���鎹㈣揣鏀跨瓥** | 鑷���鍔ㄧ瓟澶嶉������鎹㈣揣銆侀������娆炬斂绛��� |
| 鉂��� **FAQ 瑙ｇ瓟** | 甯歌���侀棶棰樻櫤鑳藉尮閰嶅拰鍥炵瓟 |
| 馃������ **瀵硅瘽璁板繂** | 鍩轰簬 ConversationSummaryBufferMemory 鐨勯暱瀵硅瘽璁板繂 |
| 馃帹 **Web UI** | Streamlit 鏋勫缓鐨勫弸濂借亰澶╃晫闈��� |
| 馃攲 **REST API** | FastAPI 鎻愪緵鏍囧噯 HTTP 鎺ュ彛 |
| 馃惓 **Docker 閮ㄧ讲** | 涓���閿���瀹瑰櫒鍖栭儴缃��� |

## 馃彈锔��� 鎶���鏈���鏋舵瀯

```
鐢ㄦ埛杈撳叆 鈫��� Streamlit UI 鈫��� FastAPI 鈫��� LangChain Agent 鈫��� OpenAI LLM
                                  鈫���
                            Tools 宸ュ叿灞���
                     鈹屸攢鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���鈹���
                     鈹��� 璁㈠崟  鈹��� 閫���鎹㈣揣 鈹��� FAQ  鈹��� 鏃堕棿  鈹���
                     鈹斺攢鈹���鈹���鈹���鈹���鈹���鈹粹攢鈹���鈹���鈹���鈹���鈹���鈹粹攢鈹���鈹���鈹���鈹���鈹���鈹粹攢鈹���鈹���鈹���鈹���鈹���鈹���
```

## 馃殌 蹇���閫熷紑濮���

### 鍓嶇疆鏉′欢

- Python 3.10+
- OpenAI API Key

### 1锔忊儯 鏈���鍦拌繍琛���

```bash
# 鍏嬮殕椤圭洰
cd 1_customer_support_agent

# 閰嶇疆鐜���澧冨彉閲���
cp .env.example .env
# 缂栬緫 .env锛屽～鍏ヤ綘鐨��� OPENAI_API_KEY

# 瀹夎���呬緷璧���
pip install -r requirements.txt

# 鍚���鍔��� API 鏈嶅姟
uvicorn app.main:app --reload
# API 杩愯���屽湪 http://localhost:8000

# 鏂扮粓绔���鍚���鍔��� Web UI
streamlit run app/ui.py
# UI 杩愯���屽湪 http://localhost:8501
```

### 2锔忊儯 Docker 閮ㄧ讲

```bash
# 缂栬緫 .env 鏂囦欢濉���鍏��� API Key
cp .env.example .env

# 涓���閿���鍚���鍔���
docker-compose up -d

# 璁块棶 UI: http://localhost:8501
# API 鏂囨。: http://localhost:8000/docs
```

### 3锔忊儯 API 璋冪敤绀轰緥

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "鏌ヤ竴涓嬭���㈠崟 ORD-2024-001 鐨勭姸鎬���", "session_id": "user123"}
)
print(response.json()["reply"])
# 杈撳嚭: 璁㈠崟 ORD-2024-001 鐘舵������: 宸插彂璐���, 棰勮���￠���佽揪: 2024-12-25, 鎵胯繍鍟���: 椤轰赴閫熻繍
```

## 馃搧 椤圭洰缁撴瀯

```
1_customer_support_agent/
鈹溾攢鈹��� app/
鈹���   鈹溾攢鈹��� __init__.py      # 閰嶇疆绠＄悊
鈹���   鈹溾攢鈹��� main.py          # FastAPI 搴旂敤鍏ュ彛
鈹���   鈹溾攢鈹��� agent.py         # LangChain Agent 鏍稿績閫昏緫
鈹���   鈹斺攢鈹��� ui.py            # Streamlit 鐢ㄦ埛鐣岄潰
鈹溾攢鈹��� knowledge_base/      # 鐭ヨ瘑搴撴枃浠剁洰褰���
鈹溾攢鈹��� .env.example         # 鐜���澧冨彉閲忔ā鏉���
鈹溾攢鈹��� requirements.txt     # Python 渚濊禆
鈹溾攢鈹��� Dockerfile           # 瀹瑰櫒鏋勫缓鏂囦欢
鈹溾攢鈹��� docker-compose.yml   # 瀹瑰櫒缂栨帓
鈹斺攢鈹��� README.md            # 椤圭洰璇存槑
```

## 鈿欙笍 鎶���鏈���瑕佺偣

1. **Agent 妯″紡**: 浣跨敤 OpenAI Tools Agent锛孡LM 鑷���涓诲喅瀹氳皟鐢ㄥ摢浜涘伐鍏���
2. **瀵硅瘽璁板繂**: ConversationSummaryBufferMemory 鑷���鍔ㄦ���荤粨闀垮���硅瘽锛屾帶鍒��� token 娑堣������
3. **宸ュ叿灏佽������**: 姣忎釜瀹㈡湇鍔熻兘灏佽���呬负鐙���绔��� Tool锛屼究浜庢墿灞���
4. **閿欒������澶勭悊**: 澶氬眰寮傚父鎹曡幏锛孉PI Key 鏈���閰嶇疆鏃惰嚜鍔ㄩ檷绾т负妯℃嫙妯″紡

## 馃摑 License

MIT
