---
marp: true
theme: singularity
size: 16:9
paginate: false
lang: ja
---

<!--
【講師紹介スライド（このコメントブロック自体は転記対象外。転記対象は最初の `_footer: ''` 行から EOF まで）】
- 講師ごとに1ファイル：`templates/instructor-<講師ID>.md`。講師ID はファイル名の <講師ID> 部分（英小文字・数字・ハイフン）。
- 企画 Issue 本文「基本情報」表の「講師」欄に講師ID を書くと（複数人はカンマ区切り。例：`yamada, tanaka`）、
  `taikenkai_slides.py wrap <deck>` が該当ファイルのスライドを表紙（_class: lead tkt）の直後に、欄の順で差し込む。
- 新しい講師を足すときは、このファイルを `templates/instructor-<講師ID>.md` にコピーして文言を書き換え、
  写真を `assets/instructors/<講師ID>.jpg` に置く（縦長推奨。左の枠に合わせて上寄せで切り抜かれる）。
  写真が未用意なら `assets/instructors/placeholder.jpg` を指しておく。
- 画像パス `../assets/instructors/` は `templates/` からも `decks/` からも同じ相対位置なので、転記時に書き換えない。
- レイアウトは `tk prof`（左に写真、右に `### 名前` → 箇条書き → 略歴の段落）。ページ番号は本編と同じく表示する。
- この front matter はこのファイル単体をプレビューするためのもの。デッキへは転記しない。
-->

<!-- _footer: '' -->
<!-- _class: tk prof -->

## 講師紹介

![講師写真](../assets/instructors/yamada.jpg)

### 山田　慎也

- 出身：広島
- 職業：ITエンジニア<br>未来技術推進協会 理事<br>Hello Coding School講師
- 略歴：

大阪大学卒業後、大手メーカーの研究所に勤務後、エンジニアとして独立。2017年に仲間と共に未来技術推進協会を設立。

<!--
講師の自己紹介（1分）。出身・職業・略歴を読み上げ、今日の体験会で担当すること（進行・デモ）を一言添える。
-->
