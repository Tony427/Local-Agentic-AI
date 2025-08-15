# Local AI Chatbot

一個簡單的本地 AI 聊天機器人，使用 Python + Ollama + Open WebUI 構建。

## 功能特性

- 🤖 本地 AI 模型 (Llama 3.2 1B)
- 💬 簡潔的聊天 API
- 🌐 Web UI 界面 (Open WebUI)
- 🐳 Docker Compose 一鍵部署
- 📝 對話歷史記錄
- ⚡ GPU 加速支持

## 技術架構

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Open WebUI    │    │  Chatbot API    │    │     Ollama      │
│   (Frontend)    │◄──►│   (FastAPI)     │◄──►│  (LLM Server)   │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 11434   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 快速開始

### 前置需求

- Docker 和 Docker Compose
- Git

### 安裝步驟

1. **克隆專案**
   ```bash
   git clone <repository-url>
   cd Local-Agentic-AI
   ```

2. **啟動服務**
   ```bash
   docker-compose up -d
   ```

3. **等待模型下載** (首次啟動需要時間)
   ```bash
   # 檢查服務狀態
   docker-compose ps
   
   # 下載 Llama 3.2 1B 模型
   docker exec ollama ollama pull llama3.2:1b
   ```

4. **訪問服務**
   - 聊天 API: http://localhost:8000
   - Open WebUI: http://localhost:3000
   - Ollama 服務: http://localhost:11434

## API 使用方法

### 聊天端點

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}'
```

**回應:**
```json
{
  "response": "I'm doing well, thank you for asking! How can I help you today?",
  "model": "llama3.2:1b"
}
```

### 健康檢查

```bash
curl http://localhost:8000/health
```

### 列出可用模型

```bash
curl http://localhost:8000/models
```

### 清除對話歷史

```bash
curl -X DELETE http://localhost:8000/chat/history
```

## 開發環境設置

如果您想要在本地開發環境中運行：

### 使用 uv (推薦)

1. **安裝 uv**
   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **安裝依賴項目**
   ```bash
   uv sync
   ```

3. **運行應用**
   ```bash
   # 確保 Ollama 正在運行
   ollama serve
   
   # 在另一個終端
   uv run python app.py
   ```

### 依賴項目

專案使用以下主要依賴項目：

- **ollama**: Ollama Python 客戶端
- **fastapi**: Web API 框架
- **uvicorn**: ASGI 服務器
- **pydantic**: 資料驗證

完整依賴項目列表請參考 `pyproject.toml`。

## 配置選項

可以通過環境變數自定義配置：

```bash
# Ollama 設定
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=llama3.2:1b

# API 設定
export API_HOST=0.0.0.0
export API_PORT=8000

# Open WebUI 設定
export WEBUI_PORT=3000

# 聊天設定
export MAX_TOKENS=2048
export TEMPERATURE=0.7
```

## Docker 指令

```bash
# 啟動所有服務
docker-compose up -d

# 停止所有服務
docker-compose down

# 查看日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f ollama
docker-compose logs -f chatbot-api
docker-compose logs -f open-webui

# 重建並啟動
docker-compose up --build -d
```

## 故障排除

### 常見問題

1. **模型下載失敗**
   ```bash
   # 手動下載模型
   docker exec ollama ollama pull llama3.2:1b
   ```

2. **服務無法啟動**
   ```bash
   # 檢查服務狀態
   docker-compose ps
   
   # 查看詳細日誌
   docker-compose logs
   ```

3. **GPU 支持**
   如果您有 NVIDIA GPU，可以修改 `docker-compose.yml`：
   ```yaml
   ollama:
     image: ollama/ollama:latest
     deploy:
       resources:
         reservations:
           devices:
             - driver: nvidia
               count: 1
               capabilities: [gpu]
   ```

## 專案結構

```
Local-Agentic-AI/
├── app.py                 # FastAPI 主應用
├── config/
│   └── settings.py        # 配置設定
├── docker-compose.yml     # Docker Compose 配置
├── Dockerfile            # Python 應用 Docker 鏡像
├── init-model.sh         # 模型初始化腳本
├── pyproject.toml        # uv 專案配置
├── uv.lock              # 依賴項目鎖定文件
├── .gitignore           # Git 忽略文件
└── README.md            # 專案說明
```

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 授權

本專案使用 MIT 授權。