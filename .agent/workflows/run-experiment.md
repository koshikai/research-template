---
description: 実験の追加、実行、結果確認の一連の手順
---

# ワークフロー: 実験の実行

新しい仮説を検証するために実験を実行する際の手順です。

## 手順

1. **設定の作成**
   - `configs/` 配下に新しい YAML ファイルを作成し、パラメータ（学習率、エポック等）を定義します。
   - 例: `configs/experiment_v1.yaml`

2. **依存関係の確認**
   - 新しいライブラリが必要な場合は、事前に `uv add` で追加します。


3. **実験の実行**
   - `poethepoet` タスクを使用して実行し、引数で設定ファイルを指定します。
   - コマンド: `uv run poe exp --config configs/experiment_v1.yaml`

4. **出力の確認**
   - `outputs/<experiment_name>/<run_id>/` に生成された結果を確認します。
   - `outputs/<experiment_name>/latest/` は直近に完了した run を指します。
   - `metrics.json` を読み取り、主要な指標を確認します。
   - ログを確認し、警告やエラーが出ていないかチェックします。

5. **レポートの同期**
   - 結果を研究報告にまとめ、run ID と保存先を記します。
