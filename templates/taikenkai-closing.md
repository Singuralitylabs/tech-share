---
marp: true
theme: singularity
size: 16:9
paginate: false
lang: ja
---

<!--
【転記ガイド（このコメントブロック自体は転記対象外。転記対象は最初の `_paginate: skip` 行から EOF まで）】
- 企画 Issue に `体験会` ラベルが付いたデッキでは、下の `_paginate: skip` 行から始まる内容を、
  デッキの最後（APPENDIX・参考スライドも含めた全スライドの後）に、順序どおり・文言を改変せずに転記する
  （省略・並べ替え禁止）。front matter とこの案内コメント自体は転記しない。
- 転記の最初（直前の既存スライドとの間）に `---` を入れ、既存の最終スライドと合体しないようにする。
- 各スライド先頭のディレクティブ（_paginate: skip と _footer: ''）も一緒に、スライドごとに転記する
  （_paginate / _footer はそのスライド1枚にしか効かないスポットディレクティブなので、複数枚に差し替えたときは
  各スライドの先頭に書く。デッキ側の `paginate: true` とタイトル入り `footer:` がそのまま乗ってしまうのを防ぐため、
  抑止しない設計にするなら、その旨を CLAUDE.md に明記してから外すこと）。
- 画像パス `../assets/taikenkai/` は `templates/` からも `decks/` からも同じ相対位置なので、転記時に書き換えない。
- この front matter はこのファイル単体をプレビューするためのもの。デッキへは転記しない。
- 冒頭用の定型スライドは `templates/taikenkai-opening.md`（別ファイル）。
- 差し替え欄（転記時に改変してよい唯一の箇所。見出し・箇条書きの型は残す）：
  1. 「今後のイベントのお知らせ」の開催日程（件数は3件を目安）
  2. 「○月の主なシンラボ活動の紹介」の見出し月と箇条書きの中身
  それ以外の文言・画像・順序は改変禁止。QR・写真を差し替えるときは `assets/taikenkai/` のファイルを置き換える。
-->

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: center -->

## AI駆動開発体験会アンケート

チャットにもURLを貼りますので、ご回答お願いします
（アンケート回答頂いた方には本スライドをお送りします）

![w:260](../assets/taikenkai/qr-survey.png)

<!--
アンケートURL（チャット貼り付け用）：
https://docs.google.com/forms/d/e/1FAIpQLSfJlSsAqvXaS6id-DIRjz9EIsMUYUnYBdpsrXkd1kOEt1i9-Q/viewform?usp=header
回答者に本スライドを送る旨を口頭でも添える。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: pair -->

## AI駆動開発体験会のご支援のお願い

本AI駆動開発 体験会を継続するため、ご支援をお願いいたします。

- 金額は任意で設定可（500円以上）
- Stripeによる安全な決済
- 決済方法：クレジットカード・Google Pay・Apple Pay
- 入力頂いたメールアドレス宛に領収書を送付

<p class="fig">
<img src="../assets/taikenkai/qr-payment.png" alt="決済用QR" width="200">
決済用リンク
</p>

<!--
決済URL（チャット貼り付け用）：https://buy.stripe.com/6oUbJ1ePw5TMgh0eQe0Fi0c
opening 3枚目とほぼ同内容。導入文だけ「本〜継続するため、」になっている。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: pair -->

## AI駆動開発体験会のご支援のお願い

![w:620](../assets/taikenkai/screenshot-payment.jpeg)

<p class="fig">
<img src="../assets/taikenkai/qr-payment.png" alt="決済用QR" width="180">
決済用リンク
</p>

<!--
決済画面のスクショ（メールアドレスは公開済みのためマスキングしない）＋同じ決済QR。
決済URL：https://buy.stripe.com/6oUbJ1ePw5TMgh0eQe0Fi0c
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: pair -->

## 今後のイベントのお知らせ

プログラミング・AI駆動開発体験会

- 8/17 (月) 20時~ Web開発講座 GASによるAPI連携体験
- 9/7 (月) 20時~ AI駆動開発講座 Web公開手法
- 9/14 (月) 20時~ Web開発講座 可視化Dashboard開発

<p class="fig">
<img src="../assets/taikenkai/qr-events.png" alt="申込フォームQR" width="200">
申込フォーム
</p>

<!--
差し替え欄：開催日程。転記時に最新の3件へ更新する。見出し「プログラミング・AI駆動開発体験会」と箇条書きの型は残す。
申込URL（チャット貼り付け用）：https://forms.gle/rq9TDREWNbZwoEAW6
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: center -->

## シンギュラリティ・ラボとは

> テクノロジーによる<br>社会課題解決を目指すコミュニティ

![w:780](../assets/taikenkai/photo-community.jpeg)

<!--
コミュニティの一言紹介。写真は集合カット（Singularity Lab の看板）。短く置いて次の「どんなコミュニティなの？」へ渡す。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: pair wide -->

## どんなコミュニティなの？

- 会員数は約50名で、技術職・文系職・学生等、多くの職種の方が参加
- 活動目的やペースは各自の自由（アプリ開発、不定期の情報収集など）
- オンライン以外に、ワーケーションや飲み会等のオフライン企画あり

<p class="fig">
<img src="../assets/taikenkai/photo-online.jpeg" alt="オンライン交流会" width="320">
オンライン交流会
<img src="../assets/taikenkai/photo-hanami.jpeg" alt="お花見の様子" width="320">
お花見の様子
</p>

<!--
多様性・各自のペース・オフライン企画の3点。写真はオンライン交流会とお花見。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: pair wide -->

## シンラボ活動のご紹介「スキルアップ講座」

**AI技術交流会・AI共有会**
週に1〜2回、生成AIを活用したアプリ開発やAIの活用方法を共有

**Web技術講座**
毎月1回、ハンズオン形式でGitやマークダウン等のWebサービススキルを学ぶ
※アーカイブ動画あり

<p class="fig">
<img src="../assets/taikenkai/screenshot-ai-meetup.jpeg" alt="AI技術交流会の解説画面" width="360">
AI技術交流会の解説画面
<img src="../assets/taikenkai/screenshot-web-course.jpeg" alt="Web技術講座の解説画面" width="360">
Web技術講座の解説画面
</p>

<!--
左が講座の説明、右がそれぞれの解説画面。アーカイブ動画があることだけ口頭で添える。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: pair wide -->

## シンラボ活動のご紹介「Sinlab Study」

自分のペースで学習するWeb学習支援サービス

**主な機能**

- 動画・スライドでの学習
- 課題提出による実践力強化
- 提出課題のAIレビュー

| デモサイト | 紹介記事 |
|:---:|:---:|
| ![w:110](../assets/taikenkai/qr-study-demo.png) | ![w:110](../assets/taikenkai/qr-study-article.png) |

<p class="fig">
<img src="../assets/taikenkai/screenshot-study-phases.jpeg" alt="フェーズ別画面" width="300">
フェーズ別画面
<img src="../assets/taikenkai/screenshot-study-review.jpeg" alt="AIレビュー画面" width="300">
AIレビュー画面
</p>

<!--
デモサイト：https://web-skillup-service.vercel.app/demo
紹介記事：https://note.com/hello_coding/n/n48ed56a1bd3c
QRの取り違えに注意（左＝デモサイト / 右＝紹介記事。元PDFの配置）。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->

## 7月の主なシンラボ活動の紹介

- AI駆動開発の解説（AI開発におけるセキュリティ設定）
- Web技術の解説講座（npmパッケージ管理の解説）
- Webアプリのチーム開発
- もくもく会

<!--
差し替え欄：見出しの月と箇条書きの中身を、転記時に直近月の活動へ更新する。箇条書き4項目の型は残す。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->

## 会費は？

| 区分 | 金額 |
|---|---|
| 入会費 | 無料 |
| 一般会員 | 3,000円／月（税込、前払い） |
| 学生会員 | 1,500円／月　※高校生、高専生は無料 |

- 支払い方法
  - クレジットカード決済のみ
  - 毎月27日に次月分を自動決済

<!--
料金は表で見せて、支払い条件は箇条書き。学生は高校生・高専生が無料である点を口頭で補う。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->

## 注意すること

- 誹謗中傷や勧誘活動などの、人の嫌がる行為は禁止
- 会員の個人情報の収集や無断での外部への開示は禁止
- 入会時の申告内容に虚偽があったり、会費を2ヶ月滞納した場合は退会となるので注意

<!--
禁止事項は3点だけ。責めずに「これだけ守れば大丈夫」のトーンで読む。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: center -->

## 最後に

> シンラボの仲間と一緒に、<br>スキルを高めて新しい価値を<br>創り出していきましょう！

<!--
クロージング。余韻を残して終える。空の split スライドは置かない（Issue #7 決定事項）。
-->
