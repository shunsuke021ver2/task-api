# CLAUDE.md

このファイルは Claude Code がこのリポジトリで作業するときの規約です。

## プロジェクト概要

学習用のタスク管理 API（Python + FastAPI）。
最終的に GitHub Actions / Docker / AWS ECS Fargate まで広げる。
現在はフェーズ 0〜1（ローカルで動く最小構成、データはメモリ保持）。

## 開発コマンド

- セットアップ: `pip install -r requirements-dev.txt`
- 起動: `uvicorn app.main:app --reload`
- テスト: `pytest`
- Lint: `ruff check .` / フォーマット: `ruff format .`

## 設計方針

- `app/main.py` は薄く保つ（アプリ生成とルーター登録のみ）。
- HTTP の関心はルーター、データアクセスはリポジトリに置く。
  ロジックが増えてきたら `app/services/` を新設する。
- データアクセスは `TaskRepository`（`app/repository.py`）のインターフェース経由。
  実装はリポジトリのメソッドとして追加し、ルーターから直接 dict などを触らない。
- ルーターはリポジトリを `Depends(get_task_repository)` で受け取る。
  具体的な実装（メモリ / DB）を知らないようにする。
- 新しいエンドポイントを足すときの順序:
  スキーマ（`schemas.py`）→ リポジトリのメソッド → ルーター → テスト。

## やらないこと（現フェーズ）

- ルーターにビジネスロジックやデータ構造の直接操作を書かない。
- DB、mypy、pre-commit、docker-compose はまだ導入しない。
- 破壊的な変更や新しい依存の追加は、理由を説明してから行う。

## テスト方針

- `tests/conftest.py` の `client` fixture を使う（テストごとに空のリポジトリを注入）。
- 正常系・バリデーションエラー（422）・not found（404）をカバーする。
