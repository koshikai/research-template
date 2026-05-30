# TeX執筆環境ガイド

本プロジェクトにおける、LuaLaTeXを用いた日本語論文・資料の執筆環境について解説します。

## ディレクトリ構成

TeX関連のファイルは `tex/` ディレクトリに用途別で整理されています。

```text
tex/
├── sotsuron/       # 卒業論文用（jlreq bookクラス / \chapter利用）
├── zemi/           # ゼミ発表資料用（jlreq articleクラス / \section利用）
└── handout/        # 卒論概要・ハンドアウト用（jlreq article / 2段組）
```

各ディレクトリ内には以下のファイルが含まれています：
- `main.tex`: メインのソースファイル
- `references.bib`: 参考文献データ (BibTeX形式)
- `.latexmkrc`: 個別のビルド設定 (LuaLaTeX用)
- `out/`: ビルド成果物 (PDF/中間ファイル) の出力先

## ビルド方法

### コマンドラインからの実行
`poethepoet` タスクとして登録されており、`uv` 経由で実行可能です。

| 用途 | コマンド | 生成されるPDF |
| :--- | :--- | :--- |
| **卒論ビルド** | `uv run poe tex-sotsuron` | `tex/sotsuron/out/main.pdf` |
| **ゼミビルド** | `uv run poe tex-zemi` | `tex/zemi/out/main.pdf` |
| **ハンドアウト** | `uv run poe tex-handout` | `tex/handout/out/main.pdf` |
| **クリーンアップ** | `uv run poe tex-clean` | (全プロジェクトの中間ファイルを削除) |

### VS Code (推奨)
拡張機能 **LaTeX Workshop** をインストールすると、以下の機能が利用可能です。

1. **自動ビルド**: ファイル保存時 (`Ctrl+S`) に自動的に PDF が更新されます。
2. **プレビュー**: `Ctrl+Alt+V` で VS Code 内に PDF プレビューを表示。
3. **相互参照**: ソースコードと PDF を `Ctrl+Click` で相互に行き来できます。

> [!NOTE]
> プロジェクトルートの `.vscode/settings.json` に、`out/` ディレクトリ対応やビルドエンジンの設定を記述済みです。

## 執筆のヒント

### 参考文献の追加
1. `references.bib` に BibTeX 形式で文献情報を追加します。
2. 本文中で `\cite{label}` を用いて引用します。
3. はじめて引用した際は、警告を解消するために一度手動ビルドすることをお勧めします。

### 図表の挿入
図を挿入する場合は、`tex/common/figures/` などの共通ディレクトリを作成して参照するか、各プロジェクトディレクトリに `figures/` を作成して参照してください。

### 特記事項
- **エンジン**: 現代的な日本語組版が可能な **LuaLaTeX** を使用しています。
- **クラス**: `jlreq` クラスを使用しており、日本語の美しさと柔軟なカスタマイズを両立しています。
