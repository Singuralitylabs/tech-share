# 12/7 MCP 回の図（decks/20261207_mcp.md 用）

`assets/mcp/*.png` の元データ。HTML＋CSS で描いて Playwright で PNG にしている（2倍解像度、背景透過）。

```bash
cd assets/mcp/src
node shot.js reach hub actors beforeafter summary   # *.png ができる（1100×430 の枠いっぱいに書き出す）
```

書き出した PNG は余白を切り詰めてから `assets/mcp/` に置く（例：Python の PIL で `getbbox()` で切り抜く）。
`beforeafter` は説明用のイメージ図で、Claude Code の実際の返答の文言ではない。

## 前提・注意

- Playwright と Chromium が導入済みであること（`node shot.js` が `require('playwright')` を使う）。
- Google Fonts（Noto Sans JP）を読み込むので、書き出し時はネット接続が必要。
- `node shot.js` が `src/` に作る `*.png` は切り抜き前の中間ファイルなので、コミットせず消す（`rm -f *.png`）。
- 図の幅（切り抜き後のアスペクト比）が変わったら、デッキ側の `![w:…]` も見直してはみ出しを PNG で確認する。
