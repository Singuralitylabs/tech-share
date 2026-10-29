#!/usr/bin/env python3
"""体験会の定型スライド（templates/taikenkai-*.md）をデッキへ転記する。

使い方（リポジトリ直下で実行）:
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py print opening
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py print closing
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py wrap decks/YYYYMMDD_topic.md

- print: 転記対象（最初の `<!-- _paginate: skip -->` 行から EOF まで）を標準出力に出す。
  front matter と転記ガイドのコメントは含まれない。
- wrap: デッキの front matter の直後に opening、末尾に closing を、継ぎ目の `---` 付きで差し込む。
  既に転記済み（opening の先頭スライドの見出しがデッキ内にある）なら何もしない。
  差し替え欄（今後のイベント・○月の活動）はテンプレートのまま入るので、転記後に最新化すること。
"""
import subprocess
import sys
from pathlib import Path

MARKER = "<!-- _paginate: skip -->"


def repo_root() -> Path:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        if (Path(out) / "templates").is_dir():
            return Path(out)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    # スクリプトの位置（.claude/skills/tech-share-deck/scripts/）から辿る
    return Path(__file__).resolve().parents[4]


def template_body(kind: str) -> str:
    path = repo_root() / "templates" / f"taikenkai-{kind}.md"
    text = path.read_text(encoding="utf-8")
    idx = text.find(MARKER)
    if idx < 0:
        sys.exit(f"{path}: `{MARKER}` が見つからない")
    return text[idx:].strip("\n") + "\n"


def split_front_matter(text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        sys.exit("デッキに front matter がない（1行目が --- ではない）")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[: i + 1]), "".join(lines[i + 1 :])
    sys.exit("front matter が閉じていない")


def first_heading(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("## "):
            return line
    return ""


def wrap(deck_path: str) -> None:
    deck = Path(deck_path)
    text = deck.read_text(encoding="utf-8")
    opening = template_body("opening")
    closing = template_body("closing")
    if first_heading(opening) and first_heading(opening) in text:
        print(f"{deck}: 定型スライドは転記済みのようなのでスキップ", file=sys.stderr)
        return
    fm, body = split_front_matter(text)
    body = body.strip("\n")
    new = f"{fm}\n{opening}\n---\n\n{body}\n\n---\n\n{closing}"
    deck.write_text(new, encoding="utf-8")
    print(f"{deck}: opening を表紙の前に、closing を末尾に転記した。差し替え欄（今後のイベントのお知らせ／○月の主なシンラボ活動の紹介）を最新化すること", file=sys.stderr)


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "print" and sys.argv[2] in ("opening", "closing"):
        sys.stdout.write(template_body(sys.argv[2]))
    elif len(sys.argv) == 3 and sys.argv[1] == "wrap":
        wrap(sys.argv[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
