# 自律型PDCAサイクルと実行プロトコル

本テンプレートは、Antigravity等のAIエージェントが自律的に**PDCA（Plan-Do-Check-Act）サイクル**を回し、研究を継続的に改善することを目的としています。

## 1. Plan (計画)
- エージェントは課題に対し、`implementation_plan.md` を作成、または `task.md` を更新して作業内容を明文化します。
- この際、**「何を成功条件とするか（Success Criteria）」**を定義させます（例：テストの全パス、特定のメトリクスの向上など）。
- **成功条件は定量化**し、評価可能な形で記述します（例：`accuracy >= 0.85`、`latency <= 200ms`）。

### 計画ファイルの最小テンプレート
```text
Title: 実験の目的
Context: 背景と仮説
Success Criteria:
  - 指標A: 目標値
  - 指標B: 目標値
Plan:
  - 手順1
  - 手順2
Risks:
  - 失敗要因と回避策
```

## 2. Do (実行: CLIベース)
- 全てのコード実行はCLI（`uv run`）を通じて行います。
- `poethepoet` により、共通のタスクは短縮コマンドで実行可能です。
- **実験の実行**: `uv run poe exp`
- スクリプトは `scripts/` 配下に集約し、引数でパラメータを受け取れるように設計します。
- 実行コマンド、使用した設定、および出力は `outputs/` にタイムスタンプ付きで保存されます。

## 3. Check (評価: 成果物確認)
- 実行結果（ログ、メトリクス、生成されたグラフ等）は `outputs/` または `data/interim/` に決まった形式で保存します。
- **Report & Visualization**: 
  - エージェントは `outputs/` のメトリクスを読み取ります。
  - 人間およびエージェントは `marimo` ノートブック（`uv run poe app`）を使用してインタラクティブに結果を可視化・分析します。
- 評価レポートには「成功条件の達成可否」と「次のアクション」を記載します。
- **Daily Research Log**:
  - 日付単位の記録は `docs/experiments/YYYY-MM-DD.md` に追記します。
  - 1実験ごとに短いサマリを残し、翌日の比較や振り返りに使います。
  - 実験完了時に `outputs/<experiment>/<timestamp>/report_request.json` が作られるので、
    AIエージェントはこれを入力として日次ログを執筆します。
  - 執筆コマンド: `uv run poe daily-report --request <path>`

### 評価レポートの推奨構成
```text
Result Summary:
  - 指標A: 実測値 (目標: XX)
  - 指標B: 実測値 (目標: XX)
Decision:
  - Pass / Fail
Next Action:
  - 改善案 or 次の実験
```

### Daily Research Log の推奨構成
```text
## YYYY-MM-DD HH:MM:SS - Experiment Name

- Summary: 1-2行の要約
- Decision: Pass/Fail/Continue
- Next Action: 次に試すこと
- Notes: 気づき、仮説、ログの要点
- Output: outputs/<experiment>/<timestamp>/
- Report: outputs/<experiment>/<timestamp>/report.md
- Params: outputs/<experiment>/<timestamp>/params.json
- Metrics: key=value
```

## 4. Act (改善)
- 評価結果が成功条件を満たさない場合、エージェントは自らエラーログを解析し、コードやパラメータを修正して `Plan` に戻ります。
- 成功した場合は、次の研究ステップ（`roadmap.md` の次の項目）へ進みます。
- 失敗時は「失敗原因」と「次に試す仮説」を明文化し、計画ファイルに追記します。

## エージェントへの指示（設計思想）
- **Log everything**: 標準出力だけでなく、重要な変数の推移などをログファイルに詳細に吐き出すよう設計させます。
- **Standardized paths**: `outputs/<experiment_name>/latest/` や `outputs/latest/` といったシンボリックリンクを用いることで、エージェントが「今何を見るべきか」を迷わないようにします。
- **Fail-fast**: 異常な値（NaN等）が検出されたら即座に停止し、エージェントに通知するアセットを用意します。
