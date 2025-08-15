# ==============================================================================
# Dockerfile - 用於建立 FastAPI 後端服務的容器映像檔
# ==============================================================================

# 基礎映像檔：使用輕量版的 Python 3.11
# python:3.11-slim 比 python:3.11 更小，適合正式環境
FROM python:3.11-slim

# 安裝 uv 套件管理工具
# 從官方 uv 映像檔複製 uv 執行檔到我們的容器中
# uv 是比 pip 更快的 Python 套件管理工具
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 設定工作目錄
# 容器內所有操作都會在這個目錄下執行
WORKDIR /app

# 複製專案檔案到容器中
# 先複製依賴檔案，利用 Docker 的分層快取機制
# 如果依賴沒變，這一層就不用重新建立
COPY pyproject.toml uv.lock ./

# 複製應用程式主檔案
COPY app.py ./

# 複製設定檔目錄（遞迴複製整個 config 資料夾）
COPY config/ ./config/

# 安裝 Python 依賴套件
# --frozen 確保使用 uv.lock 中的確切版本，保證環境一致性
RUN uv sync --frozen

# 對外開放 8000 埠
# 這告訴 Docker 這個容器會使用 8000 埠
# 實際的埠對應要在 docker-compose.yml 中設定
EXPOSE 8000

# 設定容器啟動時執行的指令
# 使用 uv run 來執行 Python 應用程式
# 這會啟動 FastAPI 服務器
CMD ["uv", "run", "python", "app.py"]