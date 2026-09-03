# Task API

学習用のタスク管理 API（Python + FastAPI）。

現在はフェーズ 0〜1：ローカルで動く最小構成。データはメモリ上に保持する（再起動で消える）。

## エンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/health` | ヘルスチェック |
| GET | `/tasks` | タスク一覧 |
| POST | `/tasks` | タスク作成 |
| PUT | `/tasks/{id}` | タスク更新（部分更新可） |
| DELETE | `/tasks/{id}` | タスク削除 |

タスクのフィールド: `id` (UUID文字列) / `title` / `description` / `done` / `created_at`

## セットアップ（Windows PowerShell）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

macOS / Linux の場合は `source .venv/bin/activate`。

## 起動

```powershell
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

### 動作確認例

```powershell
curl http://127.0.0.1:8000/health
curl -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{\"title\":\"牛乳を買う\"}'
curl http://127.0.0.1:8000/tasks
```

## テスト

```powershell
pytest
```

## Lint

```powershell
ruff check .
ruff format .
```

## ディレクトリ構成

```
app/
  main.py            アプリ生成とルーター登録
  schemas.py         Pydantic モデル（入出力）
  repository.py      TaskRepository（抽象）＋ InMemoryTaskRepository（実装）
  dependencies.py    Depends 用のリポジトリプロバイダ
  routers/
    health.py        GET /health
    tasks.py         /tasks CRUD
tests/
  conftest.py        TestClient fixture
  test_health.py
  test_tasks.py
```

## 今後の予定（このリポジトリの学習ゴール）

- [ ] GitHub Actions で CI（lint + test）
- [ ] Dockerfile でコンテナ化
- [ ] AWS ECR / ECS Fargate へデプロイ
- [ ] メモリ実装 → DB（PostgreSQL）へ Repository を差し替え
