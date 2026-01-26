# アーキテクチャ設計

AIエージェントが各ファイルの役割を誤認しないよう、明確な責務分離を行います。

## ディレクトリ構造

```text
.
├── src/
│   └── [project_name]/
├── .agent/                # AIエージェント設定
│   ├── skills/            # Anthropicスタイルのモジュール化スキル群
│   │   └── data-analysis/ # （例）高度なデータ解析スキル
│   │       ├── SKILL.md
│   │       └── scripts/
│   └── workflows/         # 再現可能な作業手順
├── scripts/               # 再現可能な実験実行の起点 (CLI)
│   ├── train.py
│   └── evaluate.py
├── outputs/               # 実験結果、ログ、プロット (エージェントがCheckする場所)
│   ├── latest/
│   └── [timestamp]/
├── notebooks/             # 試行錯誤用のJupyter Notebook
├── tests/                 # ユニットテスト、リグレッションテスト
├── data/                  # 実データ（Git管理対象外）
│   ├── raw/               # 編集不可の生データ
│   └── interim/           # 中間生成物
├── configs/               # 実験パラメータ (YAML/TOML)
└── docs/                  # 本ドキュメント群
```

## ディレクトリの責務
- `src/`: 研究ロジック本体（データ処理、モデル、評価）
- `scripts/`: CLIエントリーポイント。薄いラッパーに徹し、ロジックは `src/` に寄せる
- `configs/`: 実験設定（YAML/TOML）。コードから参照のみ
- `outputs/`: 実験成果物（ログ、メトリクス、プロット）
- `data/`: 実データ（`raw` は不変、`interim` は生成物）
- `notebooks/`: 探索用（`marimo` 推奨）。再現性の担保は `scripts/` を正とする
- `tests/`: ユニット/リグレッションテスト
- `.agent/`: エージェント設定とスキル（プロジェクト固有の知識を分離）

## `src/` の推奨構成
```text
src/[project_name]/
├── core/        # 研究対象の主要ロジック（モデル、学習）
├── data/        # データ読み込み・前処理
├── metrics/     # 評価指標
├── utils/       # 共通ユーティリティ
└── __init__.py
```

## データの流れ (Research Flow)
本プロジェクトでは以下のフローで研究を進めます。

1. **実装 (Logic)**: `src/` 配下に研究対象のコアアルゴリズムやデータ処理を実装（例: `LinearModel`）。
2. **設定 (Config)**: `configs/` に実験パラメータを記述（例: `sample.yaml`）。
3. **実験 (Experiment)**: `scripts/` から実験を実行。`outputs/` に結果（ログ、メトリクス）を保存。
   - コマンド: `uv run poe exp`
4. **分析 (Analysis)**: `notebooks/` で `marimo` を使って検証・可視化。
   - コマンド: `uv run poe app`

## 成果物の標準化
`outputs/` 配下は以下を推奨します。
```text
outputs/
└── 2025-01-01_120000/   # 例: タイムスタンプ付き
    ├── logs/            # 実行ログ
    ├── metrics.json     # 評価指標
    ├── params.json      # 実験パラメータ
    ├── artifacts/       # 生成物（モデル、プロット等）
    └── report.md        # 短い実験要約
```

## 依存関係のルール
- `scripts/` は `src/` にのみ依存し、逆方向の依存は持たない
- `notebooks/` は `src/` を読み込むが、`src/` から参照しない
- `data/raw/` は不変、`data/interim/` は生成可能

## 設定の受け渡し指針
- CLIは `--config` 引数で `configs/` を受け取る
- 実行時に読み込んだ設定は `outputs/` にコピーして保存

## AIエージェントへの配慮
- **Flat is better**: 階層が深すぎるとAIがパスを見失いやすいため、3〜4階層程度に留めます。
- **Antigravity Centric**: メインエージェントであるAntigravityが `.agent/skills` を介して専門的なタスクを自律実行することを前提とします。
- **CLI & Artifact Driven**: UI操作ではなくCLI実行と「成果物の確認」を中心に据えることで、エージェントが自律的にPDCAサイクルを回せるようにします。
- **Type Safety**: `src/` 配下は `ty` による型チェックをパスすることが必須です。これによりAIがリファクタリングを行う際の安全性が保証されます。
