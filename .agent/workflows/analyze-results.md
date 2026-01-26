---
description: marimoを用いたインタラクティブな分析と結果の要約手順
---

# ワークフロー: 結果の分析

実験で得られたデータを `marimo` を使って可視化・分析する手順です。

## 手順

1. **分析ノートの準備**
   - `notebooks/` 配下に Python ファイル（marimo形式）を用意します。
   - `ai_research_template` モジュールから必要な解析関数をインポートします。

2. **分析の実行**
// turbo
   - 編集モードで起動し、ブラウザで可視化を行います。
   - コマンド: `uv run poe edit`

3. **洞察の抽出**
   - スライダーやUIコンポーネントを使用して、異なるパラメータ条件下での挙動を観察します。
   - 特筆すべき傾向（例：「ある閾値を超えると精度が急落する」など）を特定します。

4. **レポートの出力**
   - 重要なグラフを画像として保存、またはノートブックを HTML として書き出して `outputs/` に保存します。
   - コマンド（エクスポート時）: `uv run marimo export html notebooks/analysis_sample.py > outputs/report.html`

5. **結論の共有**
   - 導き出した結論を `notify_user` や `walkthrough.md` を通じてユーザーに共有します。
