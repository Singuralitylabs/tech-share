# tech-share スライド

社内向け Tech Share 用のプレゼン資料を **Marp（Markdown → スライド）** で管理するリポジトリです。
`docs/` の企画書をもとに、`decks/` に Marp 形式の `.md` デッキを作成します。

## ディレクトリ構成

```
tech-share/
├── docs/                     # 企画書（プレゼンの骨子・台本）
│   └── YYYYMMDD_*.md
├── decks/                    # Marp デッキ本体（docs/ と同じ basename）
│   └── YYYYMMDD_*.md
├── build/                    # 書き出した生成物（再生成可能・git 管理外）
│   └── YYYYMMDD_*.html / .pdf / .pptx
├── themes/                   # 共有 Marp テーマ（デザインの実体）
│   └── singularity.css       # 社内フォーマットを再現した自己完結テーマ
├── assets/                   # テーマ画像の元データ（logo.png / title-bg.png）
├── .marprc.yml               # Marp CLI 設定（テーマ自動登録）
├── .vscode/settings.json     # VS Code / Cursor 拡張向け設定
└── README.md
```

- **`docs/`** … 企画書。タイムテーブル、各スライドの中身、「ひとことスライド文言案」などを記載。
- **`decks/`** … Marp デッキ。front matter に `theme: singularity` を書くだけでデザインが適用される。対応する企画書と同じファイル名にする運用。
- **`build/`** … 書き出し先。`-o` で明示的にここへ出す。中身はいつでも捨てて再生成できる。
- **`themes/singularity.css`** … 全デッキ共通のデザイン。社内フォーマットを CSS で再現し、ロゴ・表紙背景をデータ URI で内包した**自己完結テーマ**。デザイン変更はこのファイルを編集する（→[共有テーマ](#共有テーマ-themessingularitycss)）。
- **`assets/`** … テーマに埋め込んだ画像の元データ。テーマがデータ URI で内包しているため、レンダリング時には参照されない（保管用）。

### 命名規則

デッキと企画書は **`YYYYMMDD_<topic>.md`** で揃えます（`YYYYMMDD` は発表日）。両者が同じ basename を持つことで、
`docs/` と `decks/` の対応が一目で分かります。収録済みのデッキは `decks/` を直接見てください。

```
docs/20260101_example.md   ←→   decks/20260101_example.md
```

以降のコマンド例では、対象デッキの basename を `DECK` に入れて使います。

## 必要環境

- **Node.js**（`npx` で marp-cli を都度取得するため。グローバルインストールは不要）
- **Google Chrome**（PNG / PDF / PPTX の書き出し、プレビューウィンドウで使用）

## プレビュー方法

ターミナル（Warp など）自体はスライドを描画できません。以下のいずれかで確認します。

### A. ブラウザにライブリロード（ターミナル完結・おすすめ）

```bash
cd articles/slides/tech-share
export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
npx @marp-team/marp-cli -s decks
```

`-s`（server）で `decks/` を配信します。表示される `http://localhost:8080` をブラウザで開くと、
`.md` を保存するたびに **自動リロード** されます。サーバーは起動しっぱなしなので、別タブで動かしておくと便利です。
（8080 が埋まっている場合は `PORT=8099 npx @marp-team/marp-cli -s decks` のように変更できます）

### B. 専用プレビューウィンドウ

```bash
DECK=YYYYMMDD_topic   # ← 対象デッキの basename（decks/$DECK.md）
npx @marp-team/marp-cli -w -p "decks/$DECK.md" </dev/null
```

`-p`（preview）でウィンドウが開き、`-w`（watch）で編集を自動反映します。GUI と Chrome（`CHROME_PATH`）が必要です。

### C. Cursor / VS Code 拡張（編集しながら見るなら最良）

「**Marp for VS Code**」拡張を入れると、エディタ横にライブプレビューが出ます
（`.md` を開いて右上のプレビューアイコン、または `Cmd+Shift+V`）。

> ⚠️ このデッキは見出しの改行や kicker などで **インライン HTML（`<br>`, `<p class="kicker">` 等）** を使用しています。
> 拡張は HTML が既定で無効なため、一部が崩れて見えます。設定 **`markdown.marp.html` を `true`**（または `all`）にすると
> marp-cli の出力と一致します。marp-cli（A / B）は既定で HTML 有効のため、最終成果物と同じ見た目になります。

## 書き出し（HTML / PDF / PPTX）

**リポジトリ直下で実行**すると `.marprc.yml` が自動で読み込まれ、テーマ（`theme: singularity`）が解決されます。`--theme-set` は不要です。
デッキは `decks/` にあるのでパスを付け、書き出し先は `-o` で `build/` を指定します。

```bash
cd articles/slides/tech-share
export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DECK=YYYYMMDD_topic   # ← 対象デッキの basename（decks/$DECK.md）

# HTML
npx @marp-team/marp-cli --no-stdin "decks/$DECK.md" -o "build/$DECK.html" </dev/null

# PDF
npx @marp-team/marp-cli --no-stdin --pdf "decks/$DECK.md" -o "build/$DECK.pdf" </dev/null

# PowerPoint
npx @marp-team/marp-cli --no-stdin --pptx "decks/$DECK.md" -o "build/$DECK.pptx" </dev/null

# 各スライドを PNG 画像に（確認用。リポジトリを汚さないよう /tmp へ）
npx @marp-team/marp-cli --no-stdin --images png "decks/$DECK.md" -o /tmp/slide.png </dev/null
```

## 注意点（ハマりどころ）

- **`--no-stdin` は必須**。付けない（かつ `</dev/null` を渡さない）と、非対話シェルで marp-cli が
  **stdin 待ちのままハング** します（止まって見えるが、標準入力をブロックしているだけ）。
- **PNG / PDF / PPTX・プレビューには Chrome が必要**。`CHROME_PATH` に実行ファイルのパスを指定します（上記は macOS の例）。
- **`--allow-local-files` は不要**。ロゴ・表紙背景はテーマにデータ URI で内包しており、デッキはローカル画像を参照しません。
  将来デッキにローカル画像（スクショ等）を足す場合に備え、`.marprc.yml` に `allowLocalFiles: true` を設定済みなので、その場合もフラグは要りません。
- **拡張プレビューと最終出力の差**：Cursor/VS Code 拡張は `markdown.marp.html` を有効にしないと
  インライン HTML（`<br>` など）が反映されません。`.vscode/settings.json` で有効化済みです。
- **`!important` の上書き**：テーマは `default`（GitHub 由来）を `@import` して継承しているため、
  表・引用が淡色になる箇所を `!important` で上書きしています。色を調整する際はこの点に注意してください。
- **`-o` を省略すると `decks/` が汚れる**。`--pdf` / `--pptx` は既定でデッキの隣に書き出します。
  `.gitignore` で保険をかけていますが、`-o build/...` を付けるのが正です。
- **`.marprc.yml` に `inputDir` を足さない**。`decks/` → `build/` を自動化できそうに見えますが、設定すると
  ファイル名を渡すコマンドが全部 `[ERROR] Cannot pass files together with input directory.` で落ちます。
  1 枚だけ PNG 化して確認する手段が失われるため、パスと `-o` を都度書く方を選んでいます。
- **1 スライドに `_class` を 2 行書かない**。Marp は後勝ちで、先に書いた方が黙って捨てられます。
  複数クラスは `<!-- _class: refs split src -->` のように半角スペース区切りで 1 行にまとめてください。
- **はみ出しは警告されない**。Marp は本文が画面外へあふれても黙って切り落とします。とくに `split`
  （右パネル）は本文幅を半分にするため、項目の多いスライドで下が消えます。スライドを足したら PNG で確認を。

## 新しいデッキを作るには

1. `docs/` に企画書 `YYYYMMDD_*.md` を用意する。
2. `decks/` に **同じ basename** の Marp デッキ `.md` を作成し、front matter に `theme: singularity` を書く。
3. 企画書の「ひとことスライド文言案」を見出しに、要点は 3〜4 項目に圧縮する（1 枚 1 メッセージ）。
4. レイアウトは各スライドの `<!-- _class: ... -->` で切り替える（下記クラス一覧）。

スライド作成には Claude Code のスキル **`marp-slide`**（softaworks/agent-toolkit）を利用できますが、
デザインは常に共有テーマ `themes/singularity.css` 側で管理します（デッキにインライン `<style>` は書かない）。

## 共有テーマ（`themes/singularity.css`）

全デッキのデザインはこの 1 ファイルに集約されています。社内スライドフォーマット（「シンギュラリティ・ラボ」）を CSS で再現し、ロゴと表紙背景をデータ URI で内包した**自己完結テーマ**です。元フォーマットの PDF は、デザインを CSS に取り込み終えたため削除済みです（必要なら Git 履歴から取り出せます）。

- **先頭**：`/* @theme singularity */` ＋ `@import 'default';`（`default` テーマを継承）。
- **配色**：白背景 `#f9fafc` ＋ 濃紺→シアンのグラデーション **`#014e94` → `#66c5d2`**（見出し下線・矢印・強調）。本文は濃グレー、太字は濃紺。
- **フォント**：Noto Sans JP（本文・見出し）／ Inter（数字・ラベル）。Google Fonts から `@import`。
- **共通要素**：本文スライドは右上にロゴ（データ URI 埋め込み）、見出し下に濃紺→シアンのグラデ罫線、右下にページ番号、左上にパートラベル。
- **表紙**：ローポリ柄背景を `section.lead` にデータ URI で内包（`![bg]` は不要）。
- **PDF 3 レイアウトの対応**：1枚目→表紙（`lead`）、2枚目→本文・クロージング（既定）、3枚目→分割（`split`）。
- **レイアウトクラス**（`<!-- _class: ... -->` で指定。複数指定は半角スペース区切り、例 `refs split`）：

  | クラス | 用途 |
  |---|---|
  | `lead` | 表紙（ローポリ背景＋白文字） |
  | `stat` | 大きな数字の強調 |
  | `trend` | 推移レール（横並びカード＋矢印） |
  | `flow` | 4 段階などのステップ図 |
  | `grid` | 2×2 のカードグリッド |
  | `ba` | ビフォー / アフター表 |
  | `center` | 引用を中央に据える |
  | `refs` | 参考・注記 |
  | `split` | 右側に青グラデパネル（PDF 3枚目） |

- **図版は生レイアウト `<div>` を使わず**、Markdown ネイティブ要素（`<ol>` / `<ul>` / `<table>`）に CSS を当てて表現しています。これにより HTML 設定に依存せず描画されます。
- **パートのラベル**は `<!-- _header: 'PART 0X · ...' -->`、**発表者ノート**は各スライド末尾の `<!-- ... -->` コメントに記載しています。

### 他リポジトリ・他デッキへの再利用

テーマは自己完結（ロゴ・表紙背景を内包）しているため、他のプロジェクトでも次の 2 ステップで使えます。

1. `themes/singularity.css` をコピーする。
2. テーマを登録する（いずれか）：
   - **Marp CLI**：`.marprc.yml` に `themeSet: ["./themes"]` を書く（または `--theme-set themes/singularity.css`）。
   - **VS Code / Cursor 拡張**：`.vscode/settings.json` の `markdown.marp.themes` にパスを追加し、`markdown.marp.html: true` にする。
3. 各デッキの front matter に `theme: singularity` と書く。

## 補足：バージョン管理

生成物は `build/` にまとめ、`.gitignore` で除外しています。`docs/` `decks/` `themes/` `assets/`
`.marprc.yml` `.vscode/` はソースなので追跡します。

`.gitignore` は `build/` に加えて、`-o` の付け忘れで生成物が `decks/` に落ちた場合の保険も持っています。
確認用の PNG はリポジトリ内に出さず、`/tmp` などへ書き出してください。
