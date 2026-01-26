# Marp Presentation Ecosystem ガイド

Marp (Markdown Presentation Ecosystem) は、Markdown を使用して素早く、美しく洗練されたプレゼンテーションスライドを作成するためのツール群です。

## 1. 主な特徴

- **Markdown ベース**: 通常の Markdown 記法に加え、`---`（3つのハイフン）でスライドを区切る直感的な操作。
- **マルチフォーマット出力**: HTML, PDF, PPTX (PowerPoint), PNG/JPEG 画像などの形式に変換可能。
- **組み込みテーマ**: `default`, `gaia`, `uncover` といった洗練されたテーマが標準搭載。
- **高度なカスタマイズ**: CSS を使用したカスタムテーマの作成や、スライドごとのスタイル調整が可能。
- **開発者フレンドリー**: バージョン管理（Git）との相性が良く、VS Code との強力な連携が可能。

## 2. 環境構築方法

### A. VS Code 拡張機能 (推奨)
1. VS Code の拡張機能マーケットプレイスで **"Marp for VS Code"** を検索してインストールします。
2. `.md` ファイルの先頭に `marp: true` と記述すると、プレビュー画面でスライド形式として表示されます。

### B. Marp CLI (コマンドラインツール)
CLI を使用すると、コマンド一つで Markdown を各種フォーマットに変換できます。
```bash
# インストール (npm を使用)
npm install -g @marp-team/marp-cli

# PDF に変換
marp presentation.md --pdf -o presentation.pdf

# PowerPoint に変換
marp presentation.md --pptx -o presentation.pptx
```

## 3. 基本的な書き方

```markdown
---
marp: true
theme: default
paginate: true
header: "研究発表資料"
footer: "2026/01/26 - Kaito"
---

# プレゼンテーションタイトル

---

## 2枚目のスライド
- 箇条書き1
- 箇条書き2

---

<!-- _class: lead -->
## 視覚的に強調されたメッセージ (lead クラス)
```

## 4. 便利機能

- **ディレクティブ**: `theme`, `paginate`, `backgroundColor` などでスライド全体や個別の設定を変更。
- **画像の高度な処理**: `![width:500px](image.jpg)` のようにサイズ指定やフィルタ適用が可能。
- **背景指定**: `![bg right](background.jpg)` で背景画像を右側に配置し、左側にテキストを書くといったレイアウトが容易。
- **数式対応**: KaTeX をサポートしており、LaTeX 形式で美しい数式を記述可能。
