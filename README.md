# AI-Driven Research Template

AIエージェント（Antigravity等）と協調して研究を極限まで高速化するためのPythonプロジェクトテンプレートです。

## 特徴
- **Astral Stack**: `uv`, `ruff`, `ty` を用いた超高速開発サイクル
- **Reactive Analysis**: `marimo` によるコードと出力が常に一致するノートブック環境
- **Task Automation**: `poethepoet` による実験・分析コマンドの短縮化
- **AI-Native**: エージェントがコンテキストを把握しやすいディレクトリ構造と命名規則
- **自律型PDCA**: CLI実行と成果物（`outputs/`）の自動検証を前提としたワークフロー
- **スキル拡張**: `.agent/skills/` による専門能力のモジュール化

## ディレクトリ構造
詳細は [architecture.md](docs/architecture.md) を参照してください。

- `src/`: 研究ロジック（不変な部品、コアアルゴリズム）
- `scripts/`: 実験実行エントリーポイント（CLIから叩く薄いラッパー）
- `configs/`: 実験パラメータ
- `outputs/`: 実験結果、ログ、プロット（エージェントが評価する場所）
- `.agent/skills/`: エージェントの追加能力（指示セット・スクリプト）

## クイックスタート

### 1. 環境構築
```bash
# uvがインストールされている必要があります
uv sync
```

### 2. コード品質チェック
```bash
# Linter / Formatter / Typcheckを一括実行
uv run poe lint
uv run poe typecheck
```

### 3. 実験の実行
```bash
# サンプル実験を実行
uv run poe exp
```

### 4. 分析（marimo）
```bash
# ノートブックをアプリとして表示
uv run poe app

# ノートブックを編集モードで開く
uv run poe edit
```
※ `MARIMO_NOTEBOOK` 環境変数で対象ノートブックを切り替えできます。

## AIエージェント（Antigravity/Cursor）への指示
- **型ヒント**: 新機能の追加時には必ず `Strict` な型ヒントを付けてください。
- **PDCA**: 実験後は `outputs/` の結果を確認し、自律的に改善案（Act）を提示してください。
- **marimo検証**: ノートブック作成/更新後は `uv run --group dev poe ui-check -- --notebook notebooks/your_notebook.py` でWeb UIエラーまで確認してください。
- **計画**: 大規模な変更の前には `implementation_plan.md` を作成してユーザーと合意してください。

## ドキュメント
運用ルールの詳細は `docs/` 配下を参照してください：
- [Overview](docs/overview.md)
- [Architecture](docs/architecture.md)
- [PDCA Execution](docs/pdca_execution.md)
- [Collaboration Guide](docs/ai_collaboration.md)
- [Template Usage Guide](docs/template_guide.md) (新規プロジェクト作成時はこちら)
