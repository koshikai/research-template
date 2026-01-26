---
description: 論文PDFを画像化し、AIエージェントが視覚的に読み取ってMarkdown化する手順
---

1. `references/` ディレクトリに新しい論文PDFが配置されていることを確認します。

2. PDFを画像に変換します。
// turbo
uv run poe pdf2img

3. 生成された画像 (`references/images/<論文名>/*.png`) を、Antigravity（私）が視覚的に確認します。
   - 最初の数ページ（Introduction付近）と、図表が含まれる主要なページを重点的に確認します。

4. 確認した内容に基づいて、`references/<論文名>.md` を作成（または更新）します。
   - 論文のタイトル、著者、要約
   - 主な手法と結果
   - 重要な図表の説明と参照
   - 数式のLaTeX化
