# 12/7 MCP 回の図（decks/20261207_mcp.md 用）

`assets/mcp/*.png` の元データ。HTML＋CSS で描いて Playwright で PNG にしている（2倍解像度、背景透過）。

```bash
cd assets/mcp/src
node shot.js reach hub actors beforeafter summary   # *.png ができる（1100×430 の枠いっぱいに書き出す）
```

書き出した PNG は余白を切り詰めてから `assets/mcp/` に置く（例：Python の PIL で `getbbox()` で切り抜く）。
`beforeafter` は説明用のイメージ図で、Claude Code の実際の返答の文言ではない。
