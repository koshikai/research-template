# 実験の計画・実行・記録

1. [研究計画のひな形](templates/study.md)を `docs/studies/<study-id>.md` にコピーする。問い、比較対象、指標、停止条件を記す。
2. 設定を `configs/` に保存し、出力先を確認して実行する。

   ```bash
   uv run --locked poe exp --config configs/sample.yaml
   ```

3. `outputs/<experiment>/<run_id>/` の `manifest.json`、`params.json`、`metrics.json` を確認する。マニフェストは処理と成果物の保存が完了した時点で作られる。再試行には別の run ID を使う。
4. 報告に run ID と保存先を記す。共有が必要な成果物は保管先と保存期間を決める。コードに未コミットの変更がある run を引用する場合は、その差分も保存する。
5. 方針を変える場合は、[判断のひな形](templates/decision.md)を `docs/decisions/<id>-<topic>.md` にコピーし、理由と根拠を書く。状態や次の作業が変わったらラインカードを更新する。

`latest` は直近に完了した run を開くためのリンク。報告では個別の run を参照する。
日付別の作業メモが必要な場合は、run 内の `report_request.json` を使って作成できる。
