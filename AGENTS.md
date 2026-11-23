# AGENTS.md

README と該当するラインカードを読み、現在の問い、作業範囲、関連する判断を確認する。
研究の進め方は [実験の計画・実行・記録](docs/pdca_execution.md) に従う。

- 共有する研究ロジックは `src/`、実行 CLI は `scripts/`、設定は `configs/` に置く。
- 計画、結果、判断を記す文書では、コミットと個別の run ID を参照する。完了した run は保存し、再試行は別の run として扱う。
- 指標には単位と分母を添え、証拠を exact、empirical、exploratory のいずれかで記す。検定していない比較は観測された差として報告する。
- 保留したラインを再開するときは、ラインカードの再開条件を確認する。
- コード変更後は `uv run --locked poe typecheck` と `uv run --locked poe test` を実行する。整形は `uv run poe lint` を使う。
