# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリの性質

社内「Tech Share」向けプレゼンを **Marp**（Markdown → スライド）で管理するコンテンツリポジトリ。ビルドシステム・package.json・lint・テストは存在しない。「ソース」は Markdown、「ビルド」は Marp のレンダリング。Marp CLI はローカルに導入せず、`npx` で都度実行する。

## リポジトリの構成モデル

- `docs/YYYYMMDD_*.md` — **企画書**（骨子・台本）。タイムテーブル、各スライドの中身、見出しにそのまま使う「ひとことスライド文言案」を含む。
- `decks/YYYYMMDD_*.md` — **Marp デッキ**。対応する企画書と同じ basename を持つ。これが成果物。デッキ自身はスタイルを持たず、front matter で `theme: singularity` を指定するだけ。
- `build/` — **生成物の置き場**。`-o` で明示的にここへ書き出す。git 管理外。
- `themes/singularity.css` — **共有 Marp テーマ**。全デッキのデザイン（配色・レイアウトクラス・ロゴ・表紙背景）はここに集約されている。詳細は下記「テーマ」。
- `.marprc.yml` — Marp CLI 設定。`themeSet: ["./themes"]` によりテーマを自動登録し、`theme: singularity` を解決する。`allowLocalFiles: true` も設定済み。**`inputDir` は意図的に設定していない**（理由は下記「ハマりどころ」）。
- `.vscode/settings.json` — VS Code / Cursor の Marp 拡張向け。テーマ登録（`markdown.marp.themes`）と `markdown.marp.html: true`（インライン HTML 有効化）。
- `assets/` — テーマ画像の元データ（`logo.png`, `title-bg.png`）。**テーマにはデータ URI として埋め込み済み**のため、レンダリング時に参照されるわけではない（元素材の保管）。

デザインの元になった社内フォーマット（`スライドフォーマット.pdf`）は、`themes/singularity.css` への取り込みが完了したため削除済み。必要になったら Git 履歴（初回コミット）から取り出せる。

新しいデッキを作るとき：`docs/` に企画書を追加 → 同じ basename の `.md` を `decks/` に作成 → front matter に `theme: singularity` と書き、レイアウトは `_class` で指定する（インライン `<style>` は不要）。

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
- **`.marprc.yml` に `inputDir` を足さないこと**。`decks/` → `build/` を自動で対応付けられて一見便利だが、設定した瞬間にファイル名を渡すコマンドが全部 `[ERROR] Cannot pass files together with input directory.` で落ちる。1枚だけ PNG に書き出して見た目を確認する手段が失われるので、パスと `-o` を都度明示する方を選んでいる。
- **`_class` を1スライドに2行書かない**。Marp は後勝ちで、先に書いた方が黙って捨てられる（例：`<!-- _class: refs split -->` の直後に `<!-- _class: src -->` を書くと `refs split` が消える）。複数クラスは `<!-- _class: refs split src -->` のように半角スペース区切りで1行にまとめる。
- **`section.refs`（18px）と `section.src`（15px）は font-size が衝突する**。CSS 上 `refs` が後に定義されているため、両方を付けると 18px になる。出典のような密なリストは `src` 単独で使う。
- **`split`（右の青グラデパネル）は本文幅を半分に食う**。項目数の多いスライドに付けると、はみ出して下が見えなくなる。Marp は**はみ出しを警告しない**ので、スライドを足したら PNG で確認する。

## テーマ（`themes/singularity.css`）

全デッキのデザインはこの 1 ファイルに集約されている。社内フォーマット（「シンギュラリティ・ラボ」）を CSS で再現したもの。**自己完結**（ロゴ・表紙背景をデータ URI で内包）しているため、このファイルを他リポジトリにコピーして登録するだけで再利用できる。

- 先頭は `/* @theme singularity */` ＋ `@import 'default';`。**default テーマを継承**しているので、ページ番号などの基本挙動と、default（GitHub-markdown）由来の高詳細度な表・引用 CSS の両方が入る。後者に勝つため、表・引用の色/背景の上書きには **`!important` が必要**（意図的）。
- 配色：白 `#f9fafc`、濃紺→シアンのグラデ `#014e94 → #66c5d2`、太字＝濃紺。フォント：Noto Sans JP ＋ Inter。
- **PDF の 3 レイアウトがスライドの役割に対応**：1枚目（ローポリ表紙）→ 表紙、2枚目（白＋グラデ罫線＋ロゴ）→ 本文・クロージング、3枚目（右側の青グラデパネル）→ 最後／参考スライド。
- **レイアウトはスライドごとに `<!-- _class: ... -->` で指定**し、テーマ内の `section.<class>` で装飾する。クラス：`lead`（表紙。低ポリ背景を内包）、`stat`（大きな数字）、`trend`（シェア推移レール）、`flow`（連番ステップ図）、`grid`（2×2 カード）、`ba`（ビフォー/アフター表）、`center`（中央寄せ引用）、`refs`（参考）、`split`（右グラデパネル。併用可、例：`_class: refs split`）。複数クラスは半角スペース区切り。
- **図版は生レイアウト `<div>` を使わず、ネイティブ Markdown ＋ CSS で構築**：装飾した `<ol>`（flow）、`<ul>` グリッド、`<table>`。raw HTML が無効な環境でも描画される。
- **ブランド埋め込み**：ロゴは `--logo-uri`（データ URI、`:root` で一度定義し `section` と `section.split` で再利用）。表紙背景は `section.lead` の背景にデータ URI で内包（半透明の紺ベールを重ねて白文字を可読化）。

テーマを更新すると全デッキに反映される。デザインを変える場合はデッキではなくこのファイルを編集する。

## スライド作成の規約

- front matter に `theme: singularity`。
- 企画書の一言見出しを `##` の見出しに使い、各スライドは要点 3〜4 項目に圧縮、1 枚 1 メッセージ。
- パートの見出しは `<!-- _header: 'PART 0X · ラベル' -->`、発表者ノート（企画書の話すポイント）は各スライド末尾の `<!-- ... -->` コメントに置く。
- `marp-slide` スキル（softaworks/agent-toolkit）は導入済みだが、雛形生成の補助であり、デザインは常に共有テーマ側で管理する。
