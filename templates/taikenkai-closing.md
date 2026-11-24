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
- 並び：アンケート → ご支援 → 今後のイベント → Sinlab Study とは → 今日の続きは Sinlab Study で → Sinlab Study の始め方 →
  シンラボ本体の一言紹介（もっと深く学びたい方へ）→ 最後に → 空白の青スライド（区切り）→
  付録（どんなコミュニティ・会費・注意・フリー会員・Sinlab Knowledge）。付録もこのファイルに含めて最後に置く。
  案内の主役は Sinlab Study（自分のペースで学べるので「時間が取れない」層の入口になる）。シンラボ本体は一言に留め、
  詳細は付録で質問が出たときに見せる。
- 各スライドの `_class` に付いている `tk` は、前回の体験会資料（Google スライド）の見た目に寄せる体験会専用クラス。外さない。
- 差し替え欄（転記時に改変してよい唯一の箇所。見出し・箇条書きの型は残す）：
  1. 「今後のイベントのお知らせ」の小見出し（シリーズ名）と開催日程（件数は3〜4件が目安）
  2. 「今日の続きは「Sinlab Study」で」の本文（見出しは変えない）。その回の内容が公開済みなら
     「**今日の続きにおすすめ**<br>講座名 第N回「タイトル」」、未公開なら「**今日の内容は Sinlab Study で公開予定**<br>まずは公開中の「講座名」から」の型で書く
  3. アンケート・ご支援スライドの見出しと導入文にある体験会名「AI駆動開発」（例：「Web技術」。opening と同じ名前にそろえる。
     値は企画 Issue「基本情報」表の「体験会名」欄に書き、`taikenkai_slides.py wrap` がそこから読み取って一括で入れる）
  それ以外の文言・画像・順序は改変禁止。QR・写真を差し替えるときは `assets/taikenkai/` のファイルを置き換える。
-->

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk lg -->

## AI駆動開発体験会アンケート

チャットにもURLを貼りますので、ご回答お願いします<br>（アンケート回答頂いた方には本スライドをお送りします）

![w:430](../assets/taikenkai/qr-survey.png)

<!--
アンケートURL（チャット貼り付け用）：
https://docs.google.com/forms/d/e/1FAIpQLSfJlSsAqvXaS6id-DIRjz9EIsMUYUnYBdpsrXkd1kOEt1i9-Q/viewform?usp=header
回答者に本スライドを送る旨を口頭でも添える。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk pair -->

## AI駆動開発体験会のご支援のお願い

本AI駆動開発 体験会を継続するため、<br>ご支援をお願いいたします。

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
<!-- _class: tk pair -->

## AI駆動開発体験会のご支援のお願い

![w:560](../assets/taikenkai/screenshot-payment.jpeg)

<p class="fig">
<img src="../assets/taikenkai/qr-payment.png" alt="決済用QR" width="220">
決済用リンク
</p>

<!--
決済画面のスクショ（メールアドレスは公開済みのためマスキングしない）＋同じ決済QR。
決済URL：https://buy.stripe.com/6oUbJ1ePw5TMgh0eQe0Fi0c
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk pair lg -->

## 今後のイベントのお知らせ

**Web技術・AI駆動開発体験会**

- 10/19 (月) 20時~ 業務効率化講座 Pythonによる自動化
- 11/2 (月) 20時~ AI駆動開発講座 Skillsの利用
- 11/9 (月) 20時~ 業務効率化講座 Excel集計
- 11/16 (月) 20時~ チーム開発体験会

<p class="fig">
<img src="../assets/taikenkai/qr-events.png" alt="申込フォームQR" width="260">
申込フォーム
</p>

<!--
差し替え欄：小見出し（シリーズ名）と開催日程。転記時に最新の3〜4件へ更新する。箇条書きの「日付 (曜) 時刻~ 講座名 テーマ」の型は残す。
申込URL（チャット貼り付け用）：https://forms.gle/rq9TDREWNbZwoEAW6
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk pair wide -->

## Sinlab Study とは

**自分のペースで学べる**<br>AIレビュー付きのWeb技術学習サービス

- 動画と解説記事で学ぶ
- 課題を出すとAIがすぐレビュー
- 復習リストで振り返り

Web開発・GASなどの講座を公開中

<p class="fig">
<img src="../assets/taikenkai/screenshot-study-top.png" alt="Sinlab Study のトップ画面" width="500">
https://study.future-tech-association.org/
</p>

<!--
サービスの中身を一言ずつ：動画・記事で学ぶ → 課題を出すとAIがすぐ返してくれる → 復習リストで振り返る。
「時間が取れない」方でも、スキマ時間に自分のペースで進められる点を強調する。
提供はシンギュラリティ・ラボ（一般社団法人 未来技術推進協会）。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk msg -->

## 今日の続きは「Sinlab Study」で

**今日の続きにおすすめ**<br>○○講座 第○回「○○○○」

<!--
差し替え欄：見出しの下の本文（太字の1行＋講座の1行）。回ごとに次のどちらかの型で書く。
- その回の内容が Sinlab Study で公開済み：「**今日の続きにおすすめ**<br>講座名 第N回「タイトル」」
- その回の内容がまだ未公開：「**今日の内容は Sinlab Study で公開予定**<br>まずは公開中の「講座名」から」
  （公開予定が決まっていれば「○月公開予定」と書いてよい。近い公開中の講座が無ければ2行目は「まずは公開中の講座から」）
話すポイント：今日の続きを、スキマ時間に自分のペースで進められる場として紹介する。
サービスサイト：https://study.future-tech-association.org/
-->
---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk pair lg -->

## Sinlab Study は無料で始められます

1. QRコードからサイトを開く
2. Googleアカウントでログイン
3. お試し公開コンテンツをすぐに学習

※全コンテンツは月額1,500円（税込）

<p class="fig">
<img src="../assets/taikenkai/qr-study-service.png" alt="Sinlab Study のQR" width="260">
Sinlab Study
</p>

<!--
始め方は3ステップだけ。ログイン後すぐに、お試し公開コンテンツの閲覧・課題提出ができる（無料登録だけでは有料契約にならない）。
全コンテンツを使うときはアプリ内で有料プラン（月額1,500円・税込）を申し込む。
URL（チャット貼り付け用）：https://study.future-tech-association.org/
紹介サイト：https://sinlab.future-tech-association.org/sinlab-study/
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk pair lg -->

## もっと深く学びたい方へ

Sinlab Study を運営する<br>**シンギュラリティ・ラボ**は、<br>仲間と講座・チーム開発・<br>交流ができるコミュニティです

まずは無料の**フリー会員**から参加できます

<p class="fig">
<img src="../assets/taikenkai/qr-free-member.png" alt="フリー会員申込フォームQR" width="220">
フリー会員申込フォーム
</p>

<!--
シンラボ本体は一言で添えるだけにする（詳しくは付録のスライドで、質問が出たときに見せる）。
フリー会員申込フォーム：https://docs.google.com/forms/d/e/1FAIpQLSeW5Trd4st5TU_zMzKZeZbFE0t0B6YGxNpJ0veAnhCkhE94eA/viewform
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk msg -->

## 最後に

今日の続きは Sinlab Study で、<br>自分のペースで学んでいきましょう！

<!--
クロージング。Sinlab Study をもう一度だけ促して終える。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: split tk -->

<!--
区切りの空白スライド（右に青グラデのパネルだけ）。前回資料どおり「最後に」と付録の間に置く。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk pair lg -->

## どんなコミュニティなの？

会員数は約50名で、技術職・文系職・学生等、多くの職種の方が参加

活動目的やペースは各自の自由<br>（アプリ開発、不定期の情報収集など）

オンライン以外に、ワーケーションや飲み会等のオフライン企画あり

<p class="fig">
<img src="../assets/taikenkai/photo-online.jpeg" alt="オンライン交流会" width="240">
オンライン交流会
<img src="../assets/taikenkai/photo-hanami.jpeg" alt="お花見の様子" width="240">
お花見の様子
</p>

<!--
多様性・各自のペース・オフライン企画の3点。写真はオンライン交流会とお花見。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk big -->

## 会費は？

- 入会費　：無料
- 一般会員：3,000円／月（税込、前払い）
- 学生会員：1,500円／月　※高校生、高専生は無料
- 支払い方法
  - クレジットカード決済のみ
  - 毎月27日に次月分を自動決済

<!--
学生は高校生・高専生が無料である点を口頭で補う。
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk big -->

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
<!-- _class: tk pair -->

## フリー会員のご案内

いきなり会員になるのはハードルが高い...<br>という方に向けて“**シンラボ フリー会員**”の募集を開始しました

![w:600](../assets/taikenkai/banner-free-member.jpeg)

<p class="fig">
申し込みは<br>専用フォームから！
<img src="../assets/taikenkai/qr-free-member.png" alt="フリー会員申込フォームQR" width="200">
</p>

<!--
有料会員の前段として無料のフリー会員を案内する（Slack交流・体験会・限定資料閲覧）。
申込フォーム：https://docs.google.com/forms/d/e/1FAIpQLSeW5Trd4st5TU_zMzKZeZbFE0t0B6YGxNpJ0veAnhCkhE94eA/viewform
-->

---

<!-- _paginate: skip -->
<!-- _footer: '' -->
<!-- _class: tk pair wide -->

## シンラボ活動のご紹介「Sinlab Knowledge」

Web技術の重要な知識をまとめたサイト（会員のみアクセス可）

**主な内容**

- マークダウン・Git操作
- HTML/CSS/JavaScriptの基礎
- React等のWeb開発言語の基礎
- AI駆動開発のノウハウ

| ![w:90](../assets/taikenkai/qr-knowledge.png) |
|:---:|
| サービスサイト |

<p class="fig">
<img src="../assets/taikenkai/screenshot-knowledge.jpeg" alt="Sinlab Knowledge の画面" width="500">
https://knowledge.future-tech-association.org/
</p>

<!--
付録。質問が出たとき・時間が余ったときに見せる会員限定の学習サイト。
URL：https://knowledge.future-tech-association.org/
-->
