#!/usr/bin/env python3
"""体験会の定型スライド（templates/taikenkai-*.md）をデッキへ転記する。

使い方（リポジトリ直下で実行）:
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py print opening
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py print closing
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py wrap decks/YYYYMMDD_topic.md [--event 体験会名]

- print: 転記対象（最初の `<!-- _paginate: skip -->` 行から EOF まで）を標準出力に出す。
  front matter と転記ガイドのコメントは含まれない。
- wrap: デッキの front matter の直後に opening、末尾に closing を、継ぎ目の `---` 付きで差し込む。
  既に転記済み（opening の先頭スライドの見出しがデッキ内にある）なら何もしない。
  差し替え欄（今後のイベント・○月の活動）はテンプレートのまま入るので、転記後に最新化すること。
- --event: アンケート・ご支援スライドの見出しと導入文にある体験会名（既定「AI駆動開発」）を差し替える
  （例：--event Web技術）。print にも付けられる。
"""
import re
import subprocess
import sys
from pathlib import Path

MARKER = "<!-- _paginate: skip -->"
# 体験会名の差し替え欄。テンプレートには既定の名前で書いてあり、この見出しのスライドの中だけ差し替えてよい
EVENT_DEFAULT = "AI駆動開発"
EVENT_SLIDE_RE = re.compile(r"^## .*体験会(アンケート|のご支援のお願い)$", re.M)


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


def apply_event(body: str, name: str) -> str:
    """体験会名の差し替え欄（EVENT_SLIDE_RE の見出しを持つスライド）だけ、既定の体験会名を name に置き換える。"""
    if not name or name == EVENT_DEFAULT:
        return body
    chunks = re.split(r"(?m)^---$", body)
    return "---".join(c.replace(EVENT_DEFAULT, name) if EVENT_SLIDE_RE.search(c) else c for c in chunks)


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


def wrap(deck_path: str, event: str = "") -> None:
    deck = Path(deck_path)
    text = deck.read_text(encoding="utf-8")
    opening = apply_event(template_body("opening"), event)
    closing = apply_event(template_body("closing"), event)
    if first_heading(opening) and first_heading(opening) in text:
        print(f"{deck}: 定型スライドは転記済みのようなのでスキップ", file=sys.stderr)
        return
    fm, body = split_front_matter(text)
    body = body.strip("\n")
    new = f"{fm}\n{opening}\n---\n\n{body}\n\n---\n\n{closing}"
    deck.write_text(new, encoding="utf-8")
    print(f"{deck}: opening を表紙の前に、closing を末尾に転記した。差し替え欄（今後のイベントのお知らせ／○月の主なシンラボ活動の紹介）を最新化すること", file=sys.stderr)


def main() -> None:
    args, event = sys.argv[1:], ""
    if "--event" in args:
        i = args.index("--event")
        if i + 1 >= len(args):
            sys.exit(__doc__)
        event = args[i + 1]
        del args[i : i + 2]
    if len(args) == 2 and args[0] == "print" and args[1] in ("opening", "closing"):
        sys.stdout.write(apply_event(template_body(args[1]), event))
    elif len(args) == 2 and args[0] == "wrap":
        wrap(args[1], event)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
