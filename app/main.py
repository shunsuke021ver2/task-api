"""アプリの入口。アプリ生成とルーター登録だけを行う。

起動: uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app.routers import health, tasks


def create_app() -> FastAPI:
    app = FastAPI(title="Task API", version="0.1.0")
    app.include_router(health.router)
    app.include_router(tasks.router)
    return app


app = create_app()
