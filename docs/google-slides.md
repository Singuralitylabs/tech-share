# Markdown から Google スライドを生成する（deck）

[k1LoW/deck](https://github.com/k1LoW/deck) を使い、Markdown から Google スライドを生成するための手順書。

## Marp との使い分け

| | Marp | deck |
|---|---|---|
| 出力先 | HTML / PDF / PPTX | **Google スライド** |
| デザインの持ち主 | `themes/singularity.css` | Google スライド側のテーマ・レイアウトマスター |
| 出力後の編集 | 不可（Markdown を直して再出力） | **可能（ネイティブのスライドオブジェクト）** |
| 既存スライドとの合成 | 不可 | **可能** |

**既存の Google スライドと1本にまとめたい場合は deck を使う。** Marp の PPTX 書き出しは各スライドが全画面1枚の画像になるため、合成しても編集・再利用ができない。

デッキのファイル名は Marp 版と区別するため `decks/YYYYMMDD_*.gslides.md` とする。記法は Marp とまったく異なり、`themes/singularity.css` も効かない。

---

## 1. 準備

### deck のインストール

```
go install github.com/k1LoW/deck/cmd/deck@latest
```

`go install` の出力先（`$(go env GOPATH)/bin`）は PATH に入っていないことが多い。通っているディレクトリにリンクを張るのが簡単。

```
mkdir -p ~/.local/bin
ln -sf "$(go env GOPATH)/bin/deck" ~/.local/bin/deck
```

### OAuth の設定

Google アカウントでの操作が必要。

1. [Google Cloud Console](https://console.cloud.google.com) でプロジェクトを作成（既存のものを再利用でも可）
2. **API を2つ有効化する**
   - [Google Slides API](https://console.cloud.google.com/apis/library/slides.googleapis.com)
   - [Google Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com) ― **忘れやすいので注意**
3. 「認証情報」→「+ 認証情報を作成」→ **OAuth クライアント ID**
4. 種別は **デスクトップ アプリ** を選ぶ
5. 「Google Auth Platform / 対象」で、**自分のメールアドレスをテストユーザーに追加**する（アプリを公開する必要はない）
6. 認証情報の JSON をダウンロードし、**`credentials.json` にリネーム**して次の場所に置く

```
~/.local/share/deck/credentials.json
```

> ダウンロードしたファイルは `client_secret_….json` という名前になっている。**リネームしないと認識されない。**

### 動作確認

```
deck doctor
```

「Checking credentials file」「Checking authentication」「Checking configuration file」がすべて OK になれば準備完了。

---

## 2. 対象のプレゼンを決める

プレゼン ID は URL の次の部分。

```
https://docs.google.com/presentation/d/【プレゼンID】/edit
```

一覧から探すこともできる。

```
deck ls
```

**新規に作る場合**は既存プレゼンのテーマを引き継げる。

```
deck new decks/foo.gslides.md --base 【テーマ元のプレゼンID】 --title "タイトル"
```

**使えるレイアウト名の一覧**を確認する。デザインはすべて Google スライド側のレイアウトマスターが持つ。

```
deck ls-layouts -i 【プレゼンID】
```

---

## 3. Markdown の書き方

### 全体の形

```markdown
---
presentationID: 【プレゼンID】
title: プレゼンのタイトル
---

# 1枚目のタイトル

- 本文
- 本文

<!-- 発表者ノート -->

---

# 2枚目のタイトル
```

- **frontmatter** に `presentationID` と `title` を書く
- **行頭の `---`（ハイフン3つ以上）がページ区切り**
- **HTML コメントが発表者ノートになる**

### 見出しとプレースホルダの対応

- **各ページで最も浅い見出しがタイトル**になる（通常は `#`）
- その次のレベル（`##`）が**サブタイトル**になる
- 残りが**本文**に入る

**プレースホルダが足りないと、あふれた内容は描画されずに消える。警告は出ない。** 特別な理由がなければ「`#` タイトル1つ ＋ 本文」の形に統一しておくと、どのレイアウトでも壊れにくい。

### レイアウトの指定

JSON 形式の HTML コメントで指定する。レイアウト名は `deck ls-layouts` で確認した名前をそのまま書く。

```markdown
<!-- {"layout": "タイトルと本文"} -->
```

省略した場合は既定のレイアウトが使われる。

その他の設定：

| 設定 | 意味 |
|---|---|
| `"freeze": true` | そのページに書き込まない（次項参照） |
| `"ignore": true` | ページ自体を生成しない |
| `"skip": true` | スライドは作るが発表時にスキップする |
| `"key": "..."` | ページの安定した識別子 |

---

## 4. 既存のスライドと同居させる

### 前提：apply は Markdown に無いスライドを削除する

**プレゼンの内容は Markdown に完全に従属する。** Markdown に対応するページが無いスライドは、`deck apply` で削除される。

`{"freeze": true}` は「**そのページに書き込まない**」という意味であって、「ページが無くてもよい」ではない。**Markdown 側にもページを置いて場所を確保する必要がある。**

### 書き方

手で管理したいスライド1枚につき、Markdown 側にも場所取りのページを1つ置く。中身は空でよい。

```markdown
---

<!-- {"freeze": true} -->

<!-- 既存3枚目：会社紹介／スライド側で管理 -->

---
```

2つ目のコメントは発表者ノート扱いだが、freeze されたページには書き込まれないため、人間向けのメモとして書いておける。

### 注意点

- **freeze ページは「順序」で既存スライドに対応づけられる。** Markdown 側と Google スライド側で、freeze ページの並び順が一致している必要がある
- **Google スライド側にだけスライドを足すと、次の apply でずれるか消える。** 足すときは必ず Markdown 側にも同じ位置に freeze ページを足す
- 本編の途中に挟むなら、末尾ではなく**その位置**に freeze ページを置く

---

## 5. 適用する

```
# 通常
deck apply decks/foo.gslides.md

# 編集しながらリアルタイムに反映
deck apply --watch decks/foo.gslides.md

# 特定ページだけ（--watch とは併用不可）
deck apply -p 5 decks/foo.gslides.md
```

**ページを新規に追加する初回の apply では、内容が二重に入ることがある。** 新しいページを既存スライドの複製から作るため、古い内容が別のプレースホルダに残る。**もう一度 apply すれば解消する。初回は続けて2回実行する。**

ページ数が多いと Slides API のレート制限に当たることがある。落ちた場合は `-p` で分割して適用する。

---

## 6. 書き方の制約

既定のレイアウトで使う場合、次の要素は**レイアウトが崩れる**。いずれも本文プレースホルダの中ではなく独立した図形として配置されるため、置き場所が無いと既定位置（左上）に落ち、タイトルや本文と重なる。

| 要素 | 症状 | 代わりに |
|---|---|---|
| **表** | 左上に小さく描画され、本文と重なって判読できない | 箇条書きにする |
| **引用（`>`）** | 上部に配置され、タイトルと重なる | 太字の段落にする |

**箇条書きと段落だけで構成したページは正しく描画される。** 図表を使いたい場合は、置き場所を持つレイアウトをマスター側に用意する必要がある。

### 1ページあたりの分量

本文プレースホルダは固定サイズで、**文字数が多いと下にはみ出して切れる**。対処は2つ。

1. **レイアウトマスターの本文プレースホルダで「テキストを自動調整（縮小）」を有効にする** ― 1箇所の変更で全ページに効く
2. ページごとに内容を減らす

**はみ出しは警告されない。適用後は必ず全ページを目視で確認する。**

---

## 7. 出力の確認

PDF に書き出して確認できる。

```
deck export -i 【プレゼンID】 -o /tmp/check.pdf
```

ページを画像にして確認する場合（`brew install poppler` が必要）：

```
pdftoppm -png -r 80 -f 1 -l 5 /tmp/check.pdf /tmp/page
```

ブラウザで開く場合：

```
deck open decks/foo.gslides.md
```

---

## 8. トラブルシューティング

| 症状 | 原因と対処 |
|---|---|
| `deck: command not found` | PATH に `$(go env GOPATH)/bin` が無い。リンクを張るか PATH に追加する |
| `deck doctor` の credentials が NG | 認証ファイルの名前が `credentials.json` になっていない |
| 認証で権限エラー | Drive API が有効化されていない。Slides API だけでは足りない |
| `layout not found` | `deck ls-layouts` の名前と一致していない。レイアウト名が重複しているプレゼンでは意図しない方に当たることがある |
| 内容が二重に入る | 初回 apply の既知の挙動。もう一度 apply する |
| 内容が一部消える | プレースホルダ不足。見出し構成を減らすか、プレースホルダの多いレイアウトを使う |
| 既存スライドが消えた | Markdown に対応する freeze ページが無い。Google スライドの変更履歴から復元できる |

## 作業を始める前に

**適用先が本番のプレゼンの場合は、まずコピーを作ってそこで検証する。** apply は既存スライドを削除しうるため、初回の設定を詰める段階で本番に向けない。
