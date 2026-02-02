# Template Usage Guide

このプロジェクトは **GitHub Template Repository** として設計されています。
以下の手順に従うことで、新しい研究プロジェクトを数分でセットアップできます。

## 1. 新規プロジェクトの作成
1. GitHub上の本リポジトリのページへアクセスします。
2. **"Use this template"** ボタンをクリックし、"Create a new repository" を選択します。
3. リポジトリ名（例: `transformer-exploration`）を入力し、作成します。

## 2. ローカル環境のセットアップ
リポジトリをクローンし、プロジェクト名を設定します。

```bash
# クローン
git clone https://github.com/your-org/transformer-exploration.git
cd transformer-exploration

# 以前のパッケージ名 'ai_research_template' を、好きな名前に一括置換
# 例: 'my_research_v1' に変更する場合
uv run scripts/rename_project.py my_research_v1

# 依存関係の再同期（完了後）
uv sync
```

## 3. 初期化チェック
以下のコマンドで環境が正常か確認します。

```bash
uv run poe lint
uv run poe test
```

## 4. 自分用のカスタマイズ
- **README.md**: プロジェクトの目的や仮説に書き換えます。
- **configs/**: 不要なサンプル設定を削除し、自分の実験設定を作成します。
- **出力先**: `outputs/<experiment_name>/<timestamp>/` に統一されるため、
  `configs/` では `output_dir` か `experiment_name` を設定しておくと便利です。
- **.agent/skills/**: 研究に必要な追加スキルがあれば Antigravity に実装させます。

これで、準備は完了です！ `uv run poe exp` で実験を開始しましょう。
