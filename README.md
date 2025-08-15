# Local AI Chatbot

使用 Python + Ollama + Open WebUI 搭建的本地 AI 聊天機器人系統。

## 系統架構

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Open WebUI    │    │  FastAPI 後端   │    │     Ollama      │
│   (前端介面)     │◄──►│   (API 服務)    │◄──►│   (LLM 引擎)    │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 11434   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 功能特色

- 🤖 **本地運行**: 使用 Llama 3.2 1B 模型，資料不外洩
- 💬 **現代介面**: Open WebUI 提供類似 ChatGPT 的使用體驗  
- 🔧 **API 服務**: FastAPI 後端提供 RESTful API
- 🐳 **容器化**: Docker Compose 一鍵部署
- 📝 **會話記憶**: 支援多輪對話
- ⚡ **GPU 加速**: 自動偵測並使用 NVIDIA GPU

## 快速開始

### 系統需求

- Docker 和 Docker Compose
- 4GB+ 記憶體 (推薦 8GB)
- (可選) NVIDIA GPU + Docker GPU 支援

### 安裝步驟

1. **下載專案**
   ```bash
   git clone https://github.com/Tony427/Local-Agentic-AI.git
   cd Local-Agentic-AI
   ```

2. **啟動服務**
   ```bash
   docker-compose up -d
   ```

3. **等待模型下載** (首次啟動約需 5-10 分鐘)
   ```bash
   # 查看下載進度
   docker-compose logs -f ollama
   
   # 手動下載模型 (可選)
   docker exec ollama ollama pull llama3.2:1b
   ```

4. **開始使用**
   - 聊天介面: http://localhost:3000
   - API 文件: http://localhost:8000/docs
   - 健康檢查: http://localhost:8000/health

## 設定與配置

### 環境變數設定

建立 `.env` 檔案自訂設定：

```bash
# Ollama 設定
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b

# API 設定
API_HOST=0.0.0.0
API_PORT=8000

# 聊天參數
MAX_TOKENS=2048
TEMPERATURE=0.7
```

### GPU 支援設定

如果你有 NVIDIA GPU，修改 `docker-compose.yml` 啟用 GPU 加速：

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

## API 使用說明

### 聊天端點

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "你好，請介紹一下你自己"}'
```

回應格式：
```json
{
  "response": "你好！我是一個AI助手，運行在你的本地環境中...",
  "model": "llama3.2:1b"
}
```

### 其他端點

```bash
# 健康檢查
curl http://localhost:8000/health

# 查看可用模型
curl http://localhost:8000/models

# 清除對話記錄
curl -X DELETE http://localhost:8000/chat/history

# 查看對話記錄
curl http://localhost:8000/chat/history
```

## 測試步驟

### 1. 服務檢查

```bash
# 確認所有容器正常運行
docker-compose ps

# 檢查服務健康狀態
curl http://localhost:8000/health
```

### 2. 基本功能測試

```bash
# 測試聊天功能
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "1+1等於多少？"}'

# 測試多輪對話
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "請記住我叫小明"}'

curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "我叫什麼名字？"}'
```

### 3. Web 介面測試

1. 開啟瀏覽器前往 http://localhost:3000
2. 建立帳戶或直接開始聊天
3. 確認能正常收發訊息
4. 測試檔案上傳功能 (如果需要)

## 開發環境設定

如果你想在本地開發環境運行：

### 使用 uv (推薦)

```bash
# 安裝 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安裝相依套件
uv sync

# 啟動 Ollama (另開終端)
ollama serve

# 執行 FastAPI 服務
uv run python app.py
```

### 核心依賴

- `ollama` - Ollama Python 客戶端
- `fastapi` - Web API 框架
- `uvicorn` - ASGI 伺服器
- `pydantic` - 資料驗證

完整依賴清單見 `pyproject.toml`。

## 常用操作

### Docker 指令

```bash
# 查看即時日誌
docker-compose logs -f

# 重新啟動服務
docker-compose restart

# 停止所有服務
docker-compose down

# 重建並啟動
docker-compose up --build -d

# 清理未使用的映像
docker system prune -f
```

### 故障排除

#### 模型下載失敗
```bash
# 手動下載模型
docker exec ollama ollama pull llama3.2:1b

# 檢查可用空間
df -h
```

#### 記憶體不足
```bash
# 使用更小的模型
docker exec ollama ollama pull llama3.2:1b

# 或調整 Docker 記憶體限制
```

#### 無法連接服務
```bash
# 檢查連接埠是否被佔用
netstat -tulpn | grep :3000
netstat -tulpn | grep :8000
netstat -tulpn | grep :11434

# 重新啟動 Docker
sudo systemctl restart docker
```

#### GPU 無法使用
```bash
# 檢查 NVIDIA Docker 安裝
nvidia-smi
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```

## 專案結構

```
Local-Agentic-AI/
├── app.py                 # FastAPI 主程式
├── config/
│   └── settings.py        # 設定檔
├── docker-compose.yml     # Docker 編排設定
├── Dockerfile            # Python 容器建置
├── init-model.sh         # 模型初始化腳本
├── pyproject.toml        # Python 專案設定
├── uv.lock              # 依賴鎖定檔
└── README.md            # 專案說明
```

## 進階設定

### 效能調優

1. **模型快取**：首次下載後模型會快取在 Docker volume
2. **記憶體管理**：可在 `docker-compose.yml` 設定記憶體限制
3. **GPU 效能**：啟用 GPU 可大幅提升回應速度

### 安全考量

1. **網路設定**：預設僅監聽 localhost，生產環境請配置防火牆
2. **資料隱私**：所有對話均在本地處理，不會傳送到外部伺服器
3. **存取控制**：Open WebUI 支援使用者管理和權限控制

## 技術支援

- 🐛 **回報問題**: [GitHub Issues](https://github.com/Tony427/Local-Agentic-AI/issues)
- 📚 **Ollama 文件**: https://ollama.ai/docs
- 🌐 **Open WebUI 文件**: https://docs.openwebui.com

## 授權條款

MIT License - 詳見 LICENSE 檔案

---

**提示**: 首次啟動時模型下載需要時間，請耐心等候。如有問題歡迎提出 Issue！