# 新しいPCでの環境構築手順（ランブック）

このドキュメントは、`task-api` を含む開発環境を**別のPCで再現するための手順書**です。

> **重要な前提**：Claude Codeに同じアカウントでログインしても、会話履歴・プロジェクトのメモリファイル・設定・インストール済みツール・cloneしたリポジトリは**一切同期されません**。ログインは認証・課金のためだけのものです。環境を揃えたいものは、(a) gitにコミットして`clone`する、(b) この手順書どおりに再構築する、のどちらかで対応します。`CLAUDE.md` はこのリポジトリにコミット済みなので、`git clone` した時点で自動的に付いてきます。

---

## 0. 全体像

| レイヤー | 内容 |
|---|---|
| Windows（PowerShell） | Claude Code（VS Code拡張 + ネイティブCLI）、Git、Docker Desktop |
| WSL2 / Ubuntu | 案件での実作業環境に寄せたLinux環境。Git、Python、Node、Claude Code CLI、Docker（Desktop統合） |

Windows側とWSL側は**別々のファイルシステム・別々のツールインストール**です。どちらで作業するかで、下記の該当セクションを実施してください。

---

## 1. Claude Code のインストール（Windows）

2つの方法を**両方**入れておくと、GUI（VS Code）とCLI（ターミナル単体）の両方で使えます。

### 1-1. VS Code拡張

- VS Code を開き `Ctrl+Shift+X` → "Claude Code" を検索 → Install
- 拡張ID: `anthropic.claude-code`
- 必要要件: VS Code 1.94.0 以降
- 直接リンクでも可: `vscode:extension/anthropic.claude-code`

### 1-2. ネイティブCLIインストーラー（PowerShell）

```powershell
irm https://claude.ai/install.ps1 | iex
```

- 管理者権限不要
- インストール後は自動更新される
- 実行後は**新しいターミナルを開き直す**（PATHが古いウィンドウには反映されない）

### 1-3. 動作確認

```powershell
claude --version
claude doctor      # インストール状態の詳細チェック
```

---

## 2. Git のインストール・設定（Windows）

### 2-1. インストール

```powershell
winget install --id Git.Git -e --source winget --accept-source-agreements --accept-package-agreements
```

インストール後、PowerShellを開き直すか、以下でPATHを反映:

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
git --version
```

### 2-2. コミット用の名前・メールを設定（グローバル）

```powershell
git config --global user.name "shunsuke"
git config --global user.email "123607720+shunsuke021ver2@users.noreply.github.com"
git config --global init.defaultBranch main
```

メールは GitHub の noreply アドレスを使用（本名・個人メールを公開リポジトリの履歴に残さないため）。

---

## 3. GitHub 連携（Windows / リポジトリごと）

### 3-1. 既存リポジトリをclone

```powershell
git clone https://github.com/shunsuke021ver2/task-api.git
cd task-api
```

### 3-2. 初回pushで認証を通す（既存リポジトリに新規PCから書き込む場合）

Windows には **Git Credential Manager（GCM）** が同梱されており、`git push` 実行時に自動でブラウザ認証画面が開く。初回は対話的なターミナル（Claude Codeの非対話実行ではなく、通常のPowerShell）で1回だけ実行する:

```powershell
git push
```

→ ブラウザでGitHubログイン・認可 → 以後は認証情報がキャッシュされ、次回以降は自動で通る。

### 3-3. ゼロから新規リポジトリを作る場合

1. https://github.com/new でリポジトリ作成（README/.gitignore/LICENSEは追加しない）
2. ローカルで:
   ```powershell
   git init
   git add --all
   git commit -m "Initial commit"
   git remote add origin https://github.com/<user>/<repo>.git
   git push -u origin main
   ```

---

## 4. Docker Desktop（Windows）

```powershell
winget install --id Docker.DockerDesktop -e --source winget
```

インストール後:
1. Docker Desktop を起動し、WSLバックエンドを使う設定を確認（既定で有効）
2. **WSL側でもdockerコマンドを使いたい場合**: Docker Desktop の Settings → Resources → WSL Integration で対象ディストリ（Ubuntu）を有効化
3. 確認:
   ```powershell
   docker --version
   docker run hello-world
   ```

---

## 5. WSL2 + Ubuntu 環境構築

### 5-1. WSLとUbuntuのインストール

```powershell
wsl --install -d Ubuntu
```

既にWSLが入っている場合（Docker Desktopインストール時に一緒に入ることが多い）は状態確認のみ:

```powershell
wsl -l -v
```

初回起動時、Ubuntu内のユーザー名・パスワードを対話的に設定する(`wsl -d Ubuntu`)。

### 5-2. Ubuntu内の初期セットアップ

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-venv python3-pip curl build-essential
```

### 5-3. Git設定（WSL内はWindowsと別管理）

```bash
git config --global user.name "shunsuke"
git config --global user.email "123607720+shunsuke021ver2@users.noreply.github.com"
git config --global init.defaultBranch main
```

### 5-4. Python 3.13（本プロジェクトが要求するバージョン）

Ubuntu 22.04 標準リポジトリには Python 3.13 が無いため、deadsnakes PPA を使う:

```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.13 python3.13-venv
```

### 5-5. Node.js + Claude Code CLI（WSL）

**Node.js（nvm経由）:**
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
# 新しいシェルを開き直すか `source ~/.bashrc` 実行後
nvm install --lts
```

**Claude Code CLI（ネイティブインストーラー推奨）:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

または npm 経由（Node.js 22以降が前提）:
```bash
npm install -g @anthropic-ai/claude-code
```
※ `sudo npm install -g ...` は使わない（権限エラーの原因になる）。

確認:
```bash
claude --version
claude doctor
```

### 5-6. プロジェクトをclone

```bash
mkdir -p ~/projects && cd ~/projects
git clone https://github.com/shunsuke021ver2/task-api.git
cd task-api
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
ruff check .
```

---

## 6. 既知の問題（未解決）

### WSLからの外部HTTPS/HTTP通信がハングする

**症状**: WSL(Ubuntu)内で `ping` や DNS解決（`getent hosts`）は成功するのに、`curl`/`git clone`などの**TCP通信（80番・443番ポート）だけが接続確立の時点で無限にハングする**。

```bash
# この2つは成功する
ping github.com
getent hosts github.com

# これがハングする（Trying <IP>:443... で進まない）
curl -v https://github.com
git clone https://github.com/...
```

**切り分け結果（このPCでの状況）**:
- DNS: OK / ICMP: OK / TCP 80・443: NG（port問わず全滅）
- `.wslconfig` は未作成（デフォルト設定）
- VPNアダプタ（ExpressVPN TAP/TUN）は存在するが**切断状態**
- `vEthernet (WSL (Hyper-V firewall))` という名前のアダプタが存在 → Hyper-Vファイアウォール機能がWSLの通信を止めている可能性が高い

**疑われる原因（セキュアな管理PCで典型的）**:
1. 会社のセキュリティソフト/EDRのファイアウォール機能がWSLの仮想スイッチ(vEthernet)をブロックしている
2. 切断済みVPNアダプタの残留ルーティング
3. Windows Hyper-Vファイアウォールのポリシー

**試すべき対処（低リスクな順）**:
```powershell
# 1. WSL全体を再起動（データは消えない）
wsl --shutdown
# 少し待って再度 wsl -d Ubuntu で入り直す
```
```ini
# 2. ダメなら %USERPROFILE%\.wslconfig に以下を追加してネットワークモードを変更してみる
[wsl2]
networkingMode=mirrored
```
3. それでもダメな場合、社内IT/セキュリティ管理者に「WSLのvEthernetアダプタ／Hyper-V仮想スイッチからの通信を許可してほしい」と相談する（個人の設定変更だけでは解決しない可能性が高い）。

**この問題が起きている間の回避策**: WSL側でのgit clone・パッケージインストールが必要な作業は、Windows側（PowerShell）で行う。

---

## 7. セットアップ後の確認チェックリスト

- [ ] `claude --version` が通る（Windows / WSL 両方で使うなら両方）
- [ ] `git config --global user.name/user.email` が設定済み
- [ ] `git clone https://github.com/shunsuke021ver2/task-api.git` が成功する
- [ ] `pip install -r requirements-dev.txt` → `pytest -q` → `All passed`
- [ ] `ruff check .` → `All checks passed!`
- [ ] `docker build -t task-api:dev .` → `docker run -d -p 8000:8000 task-api:dev` → `curl http://localhost:8000/health` が `{"status":"ok"}`
- [ ] `git push` が認証エラーなく通る
