# 実装ロードマップ

以下のステップでテンプレートプロジェクトを構築します。

## 完了済みのステップ
- **Step 0-2**: 環境構築とツール設定（uv, ruff, ty, poe, marimo）の完了。
- **Step 3**: ディレクトリ構造（src, scripts, notebooks, outputs, configs）の構築。
- **Step 4**: Antigravity連携設定の初期化。
- **Step 5**: 線形回帰を用いたリサーチフローのサンプル実装完了。
- **Step 6**: CI（GitHub Actions）の導入による品質担保の自動化。

## 次のステップ（ユーザーによる実研究）
- **Step 7**: 実際の研究データの配置（`data/raw/`）。
- **Step 8**: 研究対象アルゴリズムの実装（`src/`）。
- **Step 9**: 実験の実行と分析（`poe exp`, `poe app`）。

## オプション: さらなる自動化と品質保証
- `pre-commit` フックの導入（コミット前lint/format自動実行）
- `pytest-cov` によるテストカバレッジ計測
- `ty` (Red-Knot) による型チェックのCI統合
