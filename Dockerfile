# ============================================================
# build ステージ: 依存を隔離した venv に入れる
# ============================================================
FROM python:3.13-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 依存定義だけ先にコピー → この層はコードを変えても再利用される
COPY requirements.txt .

# 本番用依存のみを venv にインストール
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install -r requirements.txt

# ============================================================
# runtime ステージ: 実行に必要な物だけを載せた軽量イメージ
# ============================================================
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# 非 root ユーザーを用意（uid 1000）
RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

# build ステージで作った venv をそのまま持ち込む
COPY --from=builder /opt/venv /opt/venv

# アプリ本体のみコピー（tests やドキュメントは含めない）
COPY app ./app

USER appuser

EXPOSE 8000

# コンテナ起動時のコマンド。--host 0.0.0.0 でコンテナ外から到達可能にする
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
