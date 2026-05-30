# AGENTS.md

このファイルは、AIエージェントが本プロジェクトを理解し、自律的に行動するためのエントリーポイントです。

## プロジェクト概要

- **名前**: `ai-research-template`
- **目的**: AIエージェントと協調して研究の試行錯誤を極限まで高速化するPythonテンプレート
- **Python**: 3.13（`pyproject.toml` / `.python-version` で固定）
- **パッケージマネージャ**: `uv`

## ディレクトリ構造と責務

| ディレクトリ | 責務 |
|-------------|------|
| `src/ai_research_template/` | 研究ロジック本体（データ処理、モデル、評価）。**変更の中心**。 |
| `scripts/` | CLIエントリーポイント。薄いラッパーに徹し、ロジックは `src/` に寄せる。 |
| `configs/` | 実験パラメータ（YAML）。コードから参照のみ。 |
| `outputs/` | 実験結果、ログ、プロット。**エージェントがCheckする場所**。 |
| `notebooks/` | 探索用（`marimo` 推奨）。再現性の担保は `scripts/` を正とする。 |
| `tests/` | ユニット/リグレッションテスト。 |
| `docs/` | 運用ルール（本ファイルを含む）。 |
| `docs/experiments/` | 日次の実験ログ（`YYYY-MM-DD.md`）。 |
| `.agent/skills/` | エージェントの追加能力（指示セット・スクリプト）。 |
| `tex/` | LaTeX（卒論・ゼミ・ハンドアウト）。 |

## 必須ツールとコマンド

全ての実行は `uv run` を通して行います。

```bash
# 依存の同期
uv sync

# コード品質チェック
uv run poe lint      # ruff format + ruff check --fix
uv run poe typecheck # ty check src scripts
uv run poe test      # pytest

# 実験実行
uv run poe exp       # scripts/run_experiment.py

# marimo（リアクティブノートブック）
uv run poe edit      # 編集モード
uv run poe app       # アプリとして表示（headless）

# 論文・資料変換
uv run poe paper     # scripts/convert_papers.py
uv run poe pdf2img   # scripts/pdf_to_images.py

# 日次レポート
uv run poe daily-report --request <path>

# LaTeX
uv run poe tex-sotsuron  # 卒論
uv run poe tex-zemi      # ゼミ資料
uv run poe tex-handout   # ハンドアウト
uv run poe tex-clean     # クリーン
```

## コード規約

- **型ヒント**: `src/` 配下の新規関数には必ず `Strict` な型ヒントを付ける（`ty` による静的解析が必須）。
- **Lint/Format**: `ruff`（line-length=88, target-version=py313）。ダブルクォート、スペース4つ。
- **テスト**: `pytest`。新機能追加時はテストも追加する。
- **Docstring**: Googleスタイル推奨（関数の目的、引数、戻り値、例外）。

## AIエージェントの行動指針

1. **計画先行**: 大規模な変更の前には `implementation_plan.md` を作成し、ユーザーと合意を取る。
2. **CLI & Artifact Driven**: UI操作ではなくCLI実行と `outputs/` の成果物確認を中心に据える。
3. **PDCAサイクル**:
   - **Plan**: `implementation_plan.md` で成功条件を定量化（例: `accuracy >= 0.85`）。
   - **Do**: `uv run poe exp` で実験。設定と結果は `outputs/<experiment>/<timestamp>/` に保存。
   - **Check**: `outputs/` のメトリクスを読み取り、`marimo` で可視化。日次ログは `docs/experiments/YYYY-MM-DD.md` に追記。
   - **Act**: 成功条件を満たさない場合はエラーログを解析し、コードやパラメータを修正してPlanに戻る。
4. **依存関係の守り方**:
   - `scripts/` → `src/` のみ依存。逆方向の依存は持たない。
   - `notebooks/` → `src/` を読み込むが、`src/` から参照しない。
   - `data/raw/` は不変、`data/interim/` は生成可能。
5. **成果物の標準化**:
   ```
   outputs/<experiment>/<timestamp>/
   ├── logs/
   ├── metrics.json
   ├── params.json
   ├── artifacts/
   └── report.md
   ```
6. **Log everything**: 標準出力だけでなく、重要な変数の推移をログファイルに詳細に出力する。
7. **Fail-fast**: 異常な値（NaN等）が検出されたら即座に停止し、エージェントに通知する。
8. **プロジェクトのリネーム推奨**: プロジェクトがデフォルトの `ai_research_template` という名前のままである場合、エージェントは優先的にユーザーへ適切なリネームを提案するか、必要に応じて `scripts/rename_project.py` を用いたリネーム作業を実施してください。

## 主なファイル

| ファイル | 用途 |
|---------|------|
| `src/ai_research_template/core.py` | 主要ロジック（モデル、学習） |
| `src/ai_research_template/data.py` | データ読み込み・前処理 |
| `src/ai_research_template/metrics.py` | 評価指標 |
| `src/ai_research_template/utils.py` | 共通ユーティリティ |
| `src/ai_research_template/main.py` | エントリーポイント |
| `scripts/run_experiment.py` | 実験実行スクリプト |
| `configs/sample.yaml` | サンプル設定 |
| `pyproject.toml` | 依存関係・ツール設定 |

## 詳細ドキュメント

- `docs/overview.md` — 設計思想と全体像
- `docs/architecture.md` — 構造と責務分離の詳細
- `docs/pdca_execution.md` — 自律型PDCAサイクルのプロトコル
- `docs/ai_collaboration.md` — エージェント協調ルール
- `docs/template_guide.md` — 新規プロジェクト作成時のガイド

---

**基本方針**: シンプルに、CLIで、成果物を `outputs/` に集約し、型安全に。
