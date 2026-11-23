# 研究プロジェクトテンプレート

Python の研究コード、ライン管理、実験の再現に必要な記録をひとつのリポジトリから始められます。
GitHub の Use this template で作成したら、[初期設定の手順](docs/template_guide.md)に沿って名前を変更し、研究の問いとラインカードへのリンクをこの README に置きます。

| 探すもの | 置き場 |
| --- | --- |
| 実装・設定 | [src/](src/)、[scripts/](scripts/)、[configs/](configs/) |
| 実験記録・判断 | [実験の手順](docs/pdca_execution.md)、[研究計画](docs/templates/study.md)、[判断](docs/templates/decision.md) |
| 原稿・発表資料 | [TeX](tex/README.md)、[Marp](docs/marp_guide.md) |

## 動作確認

```bash
uv sync --locked
uv run --locked poe test
uv run --locked poe exp --config configs/sample.yaml
```

サンプルの出力は `outputs/sample_experiment/<run_id>/` に保存されます。
`manifest.json` に実行情報、`params.json` に実際に使った設定、`metrics.json` に結果が入ります。

分析には `uv run poe app`、ノートブックの編集には `uv run poe edit` を使えます。

## 運用

- [研究ラインの登録と更新](docs/template_guide.md#5-研究ラインを登録する)
- [ディレクトリ構成](docs/architecture.md)
- [エージェントへの指示](AGENTS.md)
