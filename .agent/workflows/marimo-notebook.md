---
description: marimoノートブック作成後のUI実行チェックと報告手順
---

# ワークフロー: marimoノートブック作成

AIエージェントが `marimo` ノートブックを作成・更新したときの検証フローです。

## 手順

1. **構文ルールの確認**
   - `.agent/rules/marimo-notebook.md` に従って構文・設計を合わせます。
   - 公式チュートリアルの例は `notebooks/marimo_official/tutorials/` にあります。

2. **ノートブックの作成/更新**
   - `notebooks/` 配下に `.py` 形式で作成します。

3. **依存関係の追加**
   - 新規依存があれば `uv add` で追加します。
   - UIチェック用に `playwright` が未導入なら `uv add --dev playwright` を実行します。

4. **静的チェック**
   - `marimo check` で構造的な問題を検出します。
   - コマンド: `uv run --group dev marimo check notebooks/your_notebook.py`

5. **Web UI 実行チェック (必須)**
   - Web UIを実行し、JSエラー/console errorを検出します。
   - コマンド: `uv run --group dev poe ui-check -- --notebook notebooks/your_notebook.py`
   - 初回のみ: `uv run playwright install chromium`

6. **完了報告**
   - エラーがなければユーザーに **「できました」** と報告します。

## 付録: 卒論ボード型ノートの推奨手順
1. **UI定義セル**
   - ドロップダウン、スライダー、実行ボタン等を作成し return。
2. **UIレイアウトセル**
   - `mo.sidebar(mo.vstack([...]))` でまとめて表示。
3. **設定解決セル**
   - UI値から `dataset_name` などの設定を決定し return。
4. **データ/環境のロード**
   - `setup_experiment` 等で artifacts を読み込み return。
5. **学習実行セル**
   - `mo.stop(not run_button.value, ...)` でガード。
   - `with mo.status.spinner(...):` で学習実行。
6. **解析セル**
   - try/except で `analysis_error` を返し、結果を整形。
7. **可視化セル**
   - `mo.as_html` で図を表示、`mo.vstack` でまとめる。
8. **保存セル**
   - `mo.ui.text` + `run_button` + `mo.stop` で安全に保存。
