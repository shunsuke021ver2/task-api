# 引継ぎ資料（進捗・やり残し・作業時の約束事）

このドキュメントは、**別の環境（別PC／別セッション）に移行しても、ここまでの進捗とやり残しを見失わないため**のものです。

マシンのセットアップ自体は [docs/machine-setup.md](machine-setup.md) を参照（Claude Code / Git / Docker / WSL のインストール手順）。こちらは**プロジェクトの進め方・状態**が中心です。

最終更新: 2026-10-08 / 最新コミット: `9f3bc6a`

---

## 1. プロジェクトのゴール

学習目的は [README.md](../README.md) と [CLAUDE.md](../CLAUDE.md) に記載の通り:

- Claude Code を実務的に使う
- GitHub を使う（PRフロー、ブランチ運用）
- GitHub Actions で CI/CD を学ぶ
- Docker を使う
- AWS ECR / ECS Fargate へデプロイする
- CLAUDE.md や Skills も学ぶ
- （追加）AI-DLC（AWSのAI駆動開発ライフサイクル）を触ってみる

リポジトリ: https://github.com/shunsuke021ver2/task-api

---

## 2. これまでの進捗（完了済み）

| フェーズ | 内容 | 状態 |
|---|---|---|
| 0〜1 | FastAPI + メモリ実装で `/health`、`/tasks` CRUD。Repositoryパターンで分離。pytest 10件、ruff lint済み | ✅ |
| GitHub | リポジトリ作成、git init、初回push、PRフロー2回体験（README更新・Docker化）、両方マージ済み | ✅ |
| 2 | GitHub Actions CI（[ci.yml](../.github/workflows/ci.yml)）。`main`へのpush／PR作成時に ruff + pytest を自動実行。動作確認済み | ✅ |
| 3 | Docker化（[Dockerfile](../Dockerfile)、[.dockerignore](../.dockerignore)）。マルチステージ・非root・軽量（61.6MB）。ローカルで build → run → `/health` 応答まで確認済み | ✅ |
| - | 別PC移行用のセットアップ手順書（[machine-setup.md](machine-setup.md)）作成 | ✅ |

### 現在のリポジトリ構成（主要ファイル）

```
app/
  main.py / schemas.py / repository.py / dependencies.py
  routers/health.py, tasks.py
tests/
  conftest.py, test_health.py, test_tasks.py
.github/workflows/ci.yml
Dockerfile / .dockerignore
docs/machine-setup.md, handover.md（このファイル）
CLAUDE.md / README.md
requirements.txt / requirements-dev.txt / pyproject.toml
```

### コミット履歴

```
9f3bc6a Add machine setup runbook for Windows/WSL environment
22c80e6 Merge pull request #2 from shunsuke021ver2/feature/dockerize
977a1c5 Add Dockerfile and .dockerignore for containerized deployment
93845f8 Merge pull request #1 from shunsuke021ver2/feature/readme-update
e64727c Add learning goals line to README
5a8513c Add GitHub Actions CI (ruff + pytest on Python 3.13)
5e7c08b Add task management API (phase 0-1)
```

---

## 3. やり残しリスト（TODO）

### 本丸：AWSデプロイ系
- [ ] **CIでDockerビルドの検証**を追加（`ci.yml` に `docker build` ステップ。ECRへ進む前の安全網）
- [ ] **AWS ECR リポジトリ作成**、イメージをpush
- [ ] **AWS ECS Fargate**：クラスタ・タスク定義・サービス・ALB（ヘルスチェック先は `/health`）
- [ ] **GitHub Actions → AWS デプロイ連携**：OIDC認証（アクセスキーを置かない）、ECRへのpushジョブ、ECSデプロイジョブ

### 保守・衛生系（すぐ終わる軽作業）
- [ ] `CLAUDE.md` の更新（「フェーズ0〜1」のままなので、Docker完了などを反映）
- [ ] `.gitattributes` 追加（LF/CRLF警告の解消。Linux/Docker/CIと改行コードを統一）
- [ ] マージ済みブランチの削除：`feature/readme-update`、`feature/dockerize` がローカル・リモートに残存中

### 拡張・学習系（任意のタイミング）
- [ ] DB化（PostgreSQL等）：Repositoryパターンは準備済みなので着手しやすい
- [ ] Claude Code の Skills自作（プロジェクト専用のSkillはまだ0個）
- [ ] **AI-DLC v2 の導入・検証**（調査済み、導入は保留中）
  - 公式: https://github.com/awslabs/aidlc-workflows （MIT）
  - Claude Codeをハーネスとして直接使える（Bedrock必須ではない）
  - 導入前に `.claude/` 以下が既存 `CLAUDE.md` と衝突しないか確認すること
  - インストールスクリプトを `irm ... | iex` で直接実行する前に、内容を一度確認すること

---

## 4. 既知の問題（未解決）

**WSL(Ubuntu)からの外部TCP通信（80/443）がハングする**。詳細切り分け・対処優先順位は [machine-setup.md の「既知の問題」セクション](machine-setup.md#6-既知の問題未解決) に記録済み。回避策：WSL側でのgit clone・パッケージインストールが必要な作業はWindows側（PowerShell）で行う。

---

## 5. 作業時の約束事（新しい環境・新しいセッションでも引き継ぐこと）

ローカルの会話履歴やメモリファイルは別PC/別セッションには引き継がれないため、**ここに明文化**しておく。

- **git commit / push / GitHubへの操作（PR作成含む）は、実行前に必ず内容を説明し、ユーザーの確認を取ってから実行する**。外部サービスへの変更は特に慎重に。
- **git commit メッセージに `Co-Authored-By: Claude` 等のAI帰属トレーラーは付けない**。ユーザーが単独のコミット作者になるようにする。
- 各gitコマンドを実行する際は、**何をするコマンドか簡潔に説明する**（学習目的のため）。
- ファイルを一気に複数作る前に、**作成するファイル一覧と役割を先に説明**してから実装する。
- 新しいツール・ソフトウェアのインストール（Git、Docker、WSL関連パッケージなど）も、実行前に確認を取る。
- mainブランチへの直接pushは避け、featureブランチ→PR→マージの流れを使う（学習目的のPRフロー）。
- 設計方針・コーディング規約は [CLAUDE.md](../CLAUDE.md) に従う（Repositoryパターン維持、ルーターは薄く、DB/mypy/pre-commit/docker-composeは現フェーズでは導入しない 等）。

---

## 6. 次のセッションでの進め方（推奨）

1. 新しい環境で [machine-setup.md](machine-setup.md) に沿ってツールを揃え、リポジトリをclone
2. このファイル（`handover.md`）と `CLAUDE.md` を読んで状況を把握
3. 「3. やり残しリスト」から次の一手を選んで着手

このファイル自体も、進捗が進んだら随時更新すること（完了した項目にチェックを入れる、新しいTODOを追加する等）。
