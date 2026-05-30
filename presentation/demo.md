---
marp: true
theme: gaia
math: katex
paginate: true
header: "Marp デモ発表"
footer: "2026/01/26 - Kaito"
backgroundColor: #fff
---

# Marp によるプレゼンテーション作成

---

## 2. スライドの区切り

- スライドは `---`（3つのハイフン）で区切ります。
- このスライドは 2 枚目です。

---

## 3. 画像のレイアウト

![bg left:40%](https://images.unsplash.com/photo-1454165833767-1330084b1d96?q=80&w=2070&auto=format&fit=crop)

- `![bg left:40%]` と書くことで、背景画像を左側に 40% の幅で表示できます。
- 右側にテキストを記述できます。
- 非常に簡単にプロフェッショナルなレイアウトが作成可能です。

---

## 4. 数式 (KaTeX)

数式も美しく表示できます。

$$
E = mc^2
$$

$$
I = \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

---

## 5. まとめ

Marp を使うと：

- 内容（Markdown）に集中できる
- デザイン（テーマ）は自動適用
- Git での管理が容易
- 各種フォーマット（PDF, PPTX）への変換が可能
