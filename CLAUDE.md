# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリの性質

社内「Tech Share」向けプレゼンを **Marp**（Markdown → スライド）で管理するコンテンツリポジトリ。ビルドシステム・package.json・lint・テストは存在しない。「ソース」は Markdown、「ビルド」は Marp のレンダリング。Marp CLI はローカルに導入せず、`npx` で都度実行する。

発表の**企画は GitHub Issue** で行う（`企画` ラベル ＋ `.github/ISSUE_TEMPLATE/presentation-plan.md`）。企画書をファイルとしてコミットする運用は廃止した。

## リポジトリの構成モデル

- **企画 Issue**（`企画` ラベル）— **企画書に相当するもの**。タイムテーブル、各スライドの中身、見出しにそのまま使う「ひとことスライド文言案」、Marp 実装メモを含む。**リポジトリ内にファイルとしては存在しない**ので、GitHub MCP（`issue_read` / `list_issues` with `labels: ["企画"]`）で読み取る。テンプレートは `.github/ISSUE_TEMPLATE/presentation-plan.md`。
- `decks/YYYYMMDD_*.md` — **Marp デッキ**。これが成果物。**表紙スライドのコメントに企画 Issue の URL** を記載し、企画の最終形（話すポイント＝発表者ノート）はデッキ側に反映しきる（Issue は後から編集でき git 履歴に残らないため、デッキを自己完結させる）。デッキ自身はスタイルを持たず、front matter で `theme: singularity` を指定するだけ。
- `decks/YYYYMMDD_*.gslides.md` — **[k1LoW/deck](https://github.com/k1LoW/deck) 用デッキ**（Google スライド出力）。Marp 版とは**別物**なので混同しないこと。記法が違い（`_class` や `theme` は無く、レイアウトは `<!-- {"layout": "..."} -->`）、`themes/singularity.css` も効かない。デザインは Google スライド側のテーマ／レイアウトマスターが持つ。セットアップと運用は `docs/google-slides.md` を参照。**`deck apply` は Markdown に無いスライドを削除する**ので、Slides 側にだけ足したページは消える（詳細は手順書参照）。
- `build/` — **生成物の置き場**。`-o` で明示的にここへ書き出す。git 管理外。
- `docs/` — **リポジトリの手順書置き場**（`google-slides.md` など）。発表ごとの企画書はここには置かない。
- `templates/` — **体験会用の定型スライド群**（`taikenkai-opening.md`＝表紙直前用、`taikenkai-closing.md`＝末尾用）。企画 Issue に `体験会` ラベルが付いたデッキでは転記が**必須**（下記「体験会デッキの必須スライド」）。`decks/` に置かないのは、日付付きデッキやライブプレビュー（`-s decks`）の対象と混ざるのを避けるため。
- `themes/singularity.css` — **共有 Marp テーマ**。全デッキのデザイン（配色・レイアウトクラス・ロゴ・表紙背景）はここに集約されている。詳細は下記「テーマ」。
- `.marprc.yml` — Marp CLI 設定。`themeSet: ["./themes"]` によりテーマを自動登録し、`theme: singularity` を解決する。`allowLocalFiles: true` も設定済み。**`inputDir` は意図的に設定していない**（理由は下記「ハマりどころ」）。
- `.vscode/settings.json` — VS Code / Cursor の Marp 拡張向け。テーマ登録（`markdown.marp.themes`）と `markdown.marp.html: true`（インライン HTML 有効化）。
- `assets/` — テーマ画像の元データ（`logo.png`, `title-bg.png`）。**テーマにはデータ URI として埋め込み済み**のため、レンダリング時に参照されるわけではない（元素材の保管）。

デザインの元になった社内フォーマット（`スライドフォーマット.pdf`）は、`themes/singularity.css` への取り込みが完了したため削除済み。必要になったら Git 履歴（初回コミット）から取り出せる。旧運用の `docs/YYYYMMDD_*.md`（企画書）も Issue へ移設のうえ削除済みで、原文は Git 履歴から取り出せる。

## 企画 Issue からデッキを作る流れ

1. **企画 Issue を読む**：GitHub MCP の `issue_read`（`method: "get"`／議論は `get_comments`）で本文とコメントを取得する。どの Issue か分からない場合は `list_issues` を `labels: ["企画"]` で絞る。**Issue 本文が正、コメントは経緯**として扱い、食い違ったら本文の最新版に従う。このとき **Issue のラベルを必ず確認**し、`体験会` ラベルが付いていたら下記「体験会デッキの必須スライド」を適用する。
2. **デッキを作る**：`decks/YYYYMMDD_<topic>.md`（`YYYYMMDD` は発表日）を作成し、front matter に `theme: singularity` と書く。レイアウトは `_class` で指定する（インライン `<style>` は不要）。企画 Issue が `体験会` ラベル付きなら、`templates/taikenkai-opening.md` の定型スライド群を**表紙の直前**（デッキの物理的な先頭）に、`templates/taikenkai-closing.md` の定型スライド群を**デッキの最後**に転記する。
3. **紐付ける**：表紙スライドのコメントの先頭に `企画 Issue：https://github.com/Singuralitylabs/tech-share/issues/N` を書き、Issue 本文の「デッキ」欄にもデッキのパスを書き戻す。
4. **転記する**：企画の「話すポイント」「補足メモ」を各スライド末尾の発表者ノート（HTML コメント）に落とす。**Issue を参照しないと分からない状態にしない**。
5. **確認する**：PNG 書き出しで全スライドのはみ出しを目視確認する（下記「コマンド」）。
6. **閉じる**：コミット / PR 本文に `Closes #N` を書いて企画 Issue をクローズする。

## 体験会デッキの必須スライド（`体験会` ラベル）

体験会イベント向けの発表は、**企画 Issue に `体験会` ラベルを付けて識別**する（`list_issues` なら `labels: ["企画", "体験会"]` で絞れる）。`体験会` ラベル付きの企画から作るデッキには、以下の定型スライドを**必ず**入れる。

- **`templates/taikenkai-opening.md`** の全スライド → **表紙（lead）の直前**＝デッキの物理的な先頭。各スライドの `<!-- _paginate: false -->` `<!-- _footer: '' -->` も一緒に転記する（ページ番号・フッターが表紙より前に出ないようにするため）。
- **`templates/taikenkai-closing.md`** の全スライド → **デッキの最後**（APPENDIX・参考スライドも含めた全スライドの後）。

どちらも**全枚・順序どおり・文言を改変せず**転記する（省略・並べ替え・要約は禁止）。テンプレート側の front matter は各ファイル単体のプレビュー用なので転記しない。定型スライドの内容を変えたいときはデッキ側ではなく `templates/` のファイルを直す（次回以降のデッキに反映される。転記済みデッキには自動反映されない点に注意）。

## コマンド

先に必ず `export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"` を実行する（PDF/PPTX/PNG 書き出しとプレビューウィンドウに必要）。**必ずリポジトリ直下で実行する**（`.marprc.yml` が自動で読まれ、テーマが解決される。`--theme-set` は不要）。デッキは `decks/` にあるのでパスを付け、書き出し先は `-o` で `build/` を明示する。

```bash
# ブラウザでライブプレビュー（decks/ を HTTP 配信し、保存で自動リロード）
npx @marp-team/marp-cli -s decks

# 書き出し（HTML / PDF / PPTX）
npx @marp-team/marp-cli --no-stdin decks/20260715_ai-trend.md -o build/20260715_ai-trend.html </dev/null
npx @marp-team/marp-cli --no-stdin --pdf  decks/20260715_ai-trend.md -o build/20260715_ai-trend.pdf  </dev/null
npx @marp-team/marp-cli --no-stdin --pptx decks/20260715_ai-trend.md -o build/20260715_ai-trend.pptx </dev/null

# スライドごとの PNG（見た目の確認用。スクラッチパッドに出して Read する）
npx @marp-team/marp-cli --no-stdin --images png decks/20260715_ai-trend.md -o /tmp/slide.png </dev/null
```

デッキ変更の**視覚的な確認**は PNG 書き出しが基本手段（生成された `slide.*.png` を Read する）。確認用の PNG はリポジトリに置かず、スクラッチパッド等に出す。

`--pdf` / `--pptx` で `-o` を省略すると、生成物が**デッキの隣（`decks/`）に落ちる**。`.gitignore` で保険をかけてあるが、`-o build/...` を付けるのが正。

### 非自明なポイント（ハマりどころ）

- **`--no-stdin` と `</dev/null` は必須**。非対話シェルでは、これらが無いと marp-cli が標準入力待ちでブロックし、止まって見える（"Currently waiting data from stdin stream"）。
- **`--allow-local-files` は不要**。テーマのロゴ・表紙背景はデータ URI 埋め込みで、デッキはローカル画像を参照しない。将来デッキにローカル画像（スクショ等）を足す場合に備え、`.marprc.yml` に `allowLocalFiles: true` を入れてあるので、その場合もフラグは要らない。
- **VS Code / Cursor の Marp 拡張**は `.vscode/settings.json` でテーマ登録と `markdown.marp.html: true` を済ませてある。デッキはインライン HTML（`<br>`, `<p class="kicker">`）を使うため html 有効化が必要。
- **日本語で `**太字**` が効かないパターンがある**。閉じる `**` の**直前が `"` や `」` などの約物で、直後が文字**だと、Markdown が閉じ記号と認識せず `**` がそのまま画面に出る（例：`**AIと"作る"**ための` は失敗）。太字の範囲を語尾まで広げて `**AIと"作る"ための道具**` にすれば直る。閉じ `**` の直後が句読点なら問題ない。デッキを書いたら `grep -nE '["」』）]\*\*[^ 　]' decks/<deck>.md` で洗い出す。
- **`pre`（コードブロック）は「そのまま打ち込むコマンド」専用**。テーマの `pre` は濃紺地のターミナル風なので、キー操作（`Shift + Tab` など）をここに入れると**打ち込むものと誤解される**。キー操作は引用（`>`）＋インラインコードで書く。
- **`.marprc.yml` に `inputDir` を足さないこと**。`decks/` → `build/` を自動で対応付けられて一見便利だが、設定した瞬間にファイル名を渡すコマンドが全部 `[ERROR] Cannot pass files together with input directory.` で落ちる。1枚だけ PNG に書き出して見た目を確認する手段が失われるので、パスと `-o` を都度明示する方を選んでいる。
- **`_class` を1スライドに2行書かない**。Marp は後勝ちで、先に書いた方が黙って捨てられる（例：`<!-- _class: refs split -->` の直後に `<!-- _class: src -->` を書くと `refs split` が消える）。複数クラスは `<!-- _class: refs split src -->` のように半角スペース区切りで1行にまとめる。
- **`section.refs`（18px）と `section.src`（15px）は font-size が衝突する**。CSS 上 `refs` が後に定義されているため、両方を付けると 18px になる。出典のような密なリストは `src` 単独で使う。
- **`split`（右の青グラデパネル）は本文幅を半分に食う**。項目数の多いスライドに付けると、はみ出して下が見えなくなる。Marp は**はみ出しを警告しない**ので、スライドを足したら PNG で確認する。

## テーマ（`themes/singularity.css`）

全デッキのデザインはこの 1 ファイルに集約されている。社内フォーマット（「シンギュラリティ・ラボ」）を CSS で再現したもの。**自己完結**（ロゴ・表紙背景をデータ URI で内包）しているため、このファイルを他リポジトリにコピーして登録するだけで再利用できる。

- 先頭は `/* @theme singularity */` ＋ `@import 'default';`。**default テーマを継承**しているので、ページ番号などの基本挙動と、default（GitHub-markdown）由来の高詳細度な表・引用 CSS の両方が入る。後者に勝つため、表・引用の色/背景の上書きには **`!important` が必要**（意図的）。
- 配色：白 `#f9fafc`、濃紺→シアンのグラデ `#014e94 → #66c5d2`、太字＝濃紺。フォント：Noto Sans JP ＋ Inter。
- **PDF の 3 レイアウトがスライドの役割に対応**：1枚目（ローポリ表紙）→ 表紙、2枚目（白＋グラデ罫線＋ロゴ）→ 本文・クロージング、3枚目（右側の青グラデパネル）→ 最後／参考スライド。
- **レイアウトはスライドごとに `<!-- _class: ... -->` で指定**し、テーマ内の `section.<class>` で装飾する。クラス：`lead`（表紙。低ポリ背景を内包）、`stat`（大きな数字）、`trend`（シェア推移レール）、`flow`（連番ステップ図）、`grid`（2×2 カード）、`ba`（ビフォー/アフター表）、`center`（中央寄せ引用）、`refs`（参考）、`dense`（手順スライド用。`pre` と引用を詰めて行数を稼ぐ）、`split`（右グラデパネル。併用可、例：`_class: refs split`）。複数クラスは半角スペース区切り。
- **コード表示**：`code`（インライン＝薄グレー地に濃紺）と `pre`（ブロック＝濃紺地に白抜き＝ターミナル風）をテーマ側で定義済み。default テーマの GitHub-markdown 由来 CSS に勝つため `!important` が必要（表・引用と同じ事情）。`pre` は「参加者がそのまま打つコマンド」に見えるので、**キー操作（`Shift + Tab` など）を `pre` で書かない**（打ち込むものと誤解される）。引用か太字で表す。
- **`section.src` に表を置くときは注意**。`table{font-size:20px}` が `section.src{font-size:15px}` の継承に勝つため、テーマ側で `section.src table` を明示的に 15px に落としてある。同様の衝突は他のクラスでも起こりうる。
- **図版は生レイアウト `<div>` を使わず、ネイティブ Markdown ＋ CSS で構築**：装飾した `<ol>`（flow）、`<ul>` グリッド、`<table>`。raw HTML が無効な環境でも描画される。
- **ブランド埋め込み**：ロゴは `--logo-uri`（データ URI、`:root` で一度定義し `section` と `section.split` で再利用）。表紙背景は `section.lead` の背景にデータ URI で内包（半透明の紺ベールを重ねて白文字を可読化）。

テーマを更新すると全デッキに反映される。デザインを変える場合はデッキではなくこのファイルを編集する。

## スライド作成の規約

- front matter に `theme: singularity`。
- **表紙スライドのコメント先頭に企画 Issue の URL** を書く（デッキ → 企画の導線）。
- 企画 Issue の「ひとことスライド文言案」を `##` の見出しに使い、各スライドは要点 3〜4 項目に圧縮、1 枚 1 メッセージ。
- パートの見出しは `<!-- _header: 'PART 0X · ラベル' -->`、発表者ノート（企画 Issue の話すポイント）は各スライド末尾の `<!-- ... -->` コメントに置く。
- 企画 Issue に `体験会` ラベルが付いているデッキは、`templates/` の定型スライド群（冒頭・末尾）の転記が必須（上記「体験会デッキの必須スライド」）。
- `marp-slide` スキル（softaworks/agent-toolkit）は導入済みだが、雛形生成の補助であり、デザインは常に共有テーマ側で管理する。
