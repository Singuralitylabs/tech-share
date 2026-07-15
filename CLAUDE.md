# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## このリポジトリの性質

社内「Tech Share」向けプレゼンを **Marp**（Markdown → スライド）で管理するコンテンツリポジトリ。ビルドシステム・package.json・lint・テストは存在しない。「ソース」は Markdown、「ビルド」は Marp のレンダリング。Marp CLI はローカルに導入せず、`npx` で都度実行する。

## リポジトリの構成モデル

- `docs/YYYYMMDD_*.md` — **企画書**（骨子・台本）。タイムテーブル、各スライドの中身、見出しにそのまま使う「ひとことスライド文言案」を含む。
- リポジトリ直下の `YYYYMMDD_*.md` — **Marp デッキ**。対応する企画書と同じ basename を持つ。これが成果物。デッキ自身はスタイルを持たず、front matter で `theme: singularity` を指定するだけ。
- `themes/singularity.css` — **共有 Marp テーマ**。全デッキのデザイン（配色・レイアウトクラス・ロゴ・表紙背景）はここに集約されている。詳細は下記「テーマ」。
- `.marprc.yml` — Marp CLI 設定。`themeSet: ["./themes"]` によりテーマを自動登録し、`theme: singularity` を解決する。`allowLocalFiles: true` も設定済み。
- `.vscode/settings.json` — VS Code / Cursor の Marp 拡張向け。テーマ登録（`markdown.marp.themes`）と `markdown.marp.html: true`（インライン HTML 有効化）。
- `assets/` — テーマ画像の元データ（`logo.png`, `title-bg.png`）。**テーマにはデータ URI として埋め込み済み**のため、レンダリング時に参照されるわけではない（元素材の保管）。
- `スライドフォーマット.pdf` — デザインの元になった社内フォーマット。**デザインは `themes/singularity.css` に取り込み済みで、今後レンダリングに使わない**（解析が遅いため）。
- `*.html` / `*.pdf` / `*.pptx` — 生成物。再生成可能でソースではない。

新しいデッキを作るとき：`docs/` に企画書を追加 → 同じ basename の `.md` を直下に作成 → front matter に `theme: singularity` と書き、レイアウトは `_class` で指定する（インライン `<style>` は不要）。

## コマンド

先に必ず `export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"` を実行する（PDF/PPTX/PNG 書き出しとプレビューウィンドウに必要）。`npx marp` はリポジトリ直下で実行すると `.marprc.yml` を自動で読み込むため、`--theme-set` は不要。

```bash
# ブラウザでライブプレビュー（ディレクトリを HTTP 配信し、保存で自動リロード）
npx @marp-team/marp-cli -s .

# 書き出し（HTML / PDF / PPTX / スライドごとの PNG）
npx @marp-team/marp-cli --no-stdin 20260715_ai-trend.md -o 20260715_ai-trend.html </dev/null
npx @marp-team/marp-cli --no-stdin --pdf      20260715_ai-trend.md </dev/null
npx @marp-team/marp-cli --no-stdin --pptx     20260715_ai-trend.md </dev/null
npx @marp-team/marp-cli --no-stdin --images png 20260715_ai-trend.md -o slide.png </dev/null
```

デッキ変更の**視覚的な確認**は PNG 書き出しが基本手段（生成された `slide.*.png` を Read する）。

### 非自明なポイント（ハマりどころ）

- **`--no-stdin` と `</dev/null` は必須**。非対話シェルでは、これらが無いと marp-cli が標準入力待ちでブロックし、止まって見える（"Currently waiting data from stdin stream"）。
- **`--allow-local-files` は不要**。テーマのロゴ・表紙背景はデータ URI 埋め込みで、デッキはローカル画像を参照しない。将来デッキにローカル画像（スクショ等）を足す場合に備え、`.marprc.yml` に `allowLocalFiles: true` を入れてあるので、その場合もフラグは要らない。
- **VS Code / Cursor の Marp 拡張**は `.vscode/settings.json` でテーマ登録と `markdown.marp.html: true` を済ませてある。デッキはインライン HTML（`<br>`, `<p class="kicker">`）を使うため html 有効化が必要。

## テーマ（`themes/singularity.css`）

全デッキのデザインはこの 1 ファイルに集約されている。社内フォーマット（`スライドフォーマット.pdf`「シンギュラリティ・ラボ」）を CSS で再現したもの。**自己完結**（ロゴ・表紙背景をデータ URI で内包）しているため、このファイルを他リポジトリにコピーして登録するだけで再利用できる。

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
