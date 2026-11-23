# 研究プロジェクトテンプレート

GitHub の Use this template でリポジトリを作成し、クローン先で次を実行します。手順には Python と uv が必要です。

```bash
uv run --no-project python scripts/rename_project.py my_research
uv sync --locked
uv run --locked poe test
uv run --locked poe exp --config configs/sample.yaml
```

`my_research` はプロジェクトに合わせて変更します。初期設定が済んだら、この README に研究の目的とラインカードへのリンクを置きます。

## 研究ライン

[ラインカード](docs/templates/research-line.md)を `docs/lines/<line-id>.md` にコピーします。複数のリポジトリを使うラインでは、カードを置く場所を一つに決め、各 README から同じカードにリンクします。次の作業や状態を決めたときに、カードの更新日と判断へのリンクを更新します。

| 記録 | 置き場 |
| --- | --- |
| 研究計画と結果 | [ひな形](docs/templates/study.md)を `docs/studies/` にコピー |
| 方針と判断理由 | [ひな形](docs/templates/decision.md)を `docs/decisions/` にコピー |
| 実験設定と実装 | [configs/](configs/)、[src/](src/)、[scripts/](scripts/) |

## 実験

1. 実行前に、問い、比較対象、指標、判断基準を研究計画に書きます。
2. `configs/` に設定を保存して実行します。出力は `outputs/<experiment>/<run_id>/` に作られます。
3. 完了後に `manifest.json`、`params.json`、`metrics.json` を確認します。報告には個別の run ID と保存先を記します。未コミットの変更がある run を引用する場合は、差分も保存します。

`outputs/` は Git の追跡対象外です。共有が必要な成果物の保管先は、研究報告に記します。再試行には別の run ID を使います。
