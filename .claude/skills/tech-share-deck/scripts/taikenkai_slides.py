#!/usr/bin/env python3
"""体験会の定型スライド（templates/taikenkai-*.md）をデッキへ転記する。

使い方（リポジトリ直下で実行）:
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py print opening
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py print closing
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py wrap decks/YYYYMMDD_topic.md [--issue N | --issue-file 本文.md | --event 体験会名]
  python3 .claude/skills/tech-share-deck/scripts/taikenkai_slides.py event (--issue N | --issue-file 本文.md)

- print: 転記対象（最初の `<!-- _paginate: skip -->` 行から EOF まで）を標準出力に出す。
  front matter と転記ガイドのコメントは含まれない。
- wrap: デッキの front matter の直後に opening、末尾に closing を、継ぎ目の `---` 付きで差し込む。
  表紙（`_class: lead tkt`）の見出し `# <体験会名> 体験会` も、定型スライドと同じ体験会名で書き換える。
  既に転記済み（opening の先頭スライドの見出しがデッキ内にある）なら何もしない。
  差し替え欄（今後のイベント・○月の活動）はテンプレートのまま入るので、転記後に最新化すること。
- 体験会名：アンケート・ご支援スライドの見出しと導入文にある体験会名（テンプレートでは「AI駆動開発」）は、
  企画 Issue 本文「基本情報」表の「体験会名」欄から取る。wrap は次の順で決める：
    --event 名前（直接指定） > --issue-file（Issue 本文を保存したファイル） > --issue N > デッキ表紙コメントの企画 Issue URL
  --issue / 表紙 URL からの取得には gh CLI（`gh issue view`）を使う。gh が無い環境では、Issue 本文を
  GitHub MCP の issue_read で取ってファイルに保存し --issue-file で渡すか、欄の値を --event で渡す。
  どれでも体験会名が決まらなければ転記しない（既定名のまま別の回に出るのを防ぐため）。
  表紙が `lead tkt` でない（旧形式の `lead` だけ）ときは表紙に触れず、その旨を表示する。
- event: Issue から読んだ体験会名を表示するだけ（確認用）。
- print にも --event / --issue / --issue-file を付けられる。
"""
import re
import subprocess
import sys
from pathlib import Path

MARKER = "<!-- _paginate: skip -->"
# 体験会名の差し替え欄。テンプレートには既定の名前で書いてあり、この見出しのスライドの中だけ差し替えてよい
EVENT_DEFAULT = "AI駆動開発"
EVENT_SLIDE_RE = re.compile(r"^## .*体験会(アンケート|のご支援のお願い)$", re.M)
REPO = "Singuralitylabs/tech-share"
ISSUE_URL_RE = re.compile(r"企画 Issue：https://github\.com/Singuralitylabs/tech-share/issues/(\d+)")
# 企画 Issue 本文「基本情報」表の行：| 体験会名 | Web技術 |
EVENT_ROW_RE = re.compile(r"^\|\s*体験会名\s*\|\s*(.*?)\s*\|\s*$", re.M)
# 体験会デッキの表紙（`_class: lead tkt`）の見出し：# <体験会名> 体験会
COVER_TITLE_RE = re.compile(r"^# (.*?)\s*体験会\s*$")
CLASS_LINE_RE = re.compile(r"^<!--\s*_class:\s*(.*?)\s*-->\s*$")


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


def event_from_issue_body(body: str) -> str:
    """企画 Issue 本文の「体験会名」欄の値。空欄・記入例（「例：」で始まる）のままなら空文字。"""
    m = EVENT_ROW_RE.search(body)
    if not m:
        return ""
    value = re.sub(r"<!--.*?-->", "", m.group(1)).strip().strip("`")
    return "" if not value or value.startswith("例") else value


def fetch_issue_body(number: str) -> str:
    try:
        return subprocess.run(
            ["gh", "issue", "view", number, "--repo", REPO, "--json", "body", "-q", ".body"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        sys.exit(f"企画 Issue #{number} を gh で取得できなかった（{e}）。"
                 "Issue 本文をファイルに保存して --issue-file で渡すか、体験会名を --event で渡す")


def resolve_event(opts: dict, deck_text: str = "") -> str:
    """--event > --issue-file > --issue > デッキ表紙の企画 Issue URL の順に体験会名を決める。決まらなければ終了する。"""
    if opts.get("event"):
        return opts["event"]
    if opts.get("issue_file"):
        body, where = Path(opts["issue_file"]).read_text(encoding="utf-8"), opts["issue_file"]
    else:
        number = opts.get("issue")
        if not number:
            m = ISSUE_URL_RE.search(deck_text)
            number = m.group(1) if m else ""
        if not number:
            sys.exit("体験会名が決まらない：--issue N / --issue-file / --event のどれかを付けるか、"
                     "表紙コメントに企画 Issue の URL を書いてから転記する")
        body, where = fetch_issue_body(number), f"企画 Issue #{number}"
    event = event_from_issue_body(body)
    if not event:
        sys.exit(f"{where} の「基本情報」表に「体験会名」が書かれていない（空欄・記入例のまま）。"
                 "Issue に記入するか、--event で渡す")
    return event


def split_front_matter(text: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        sys.exit("デッキに front matter がない（1行目が --- ではない）")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[: i + 1]), "".join(lines[i + 1 :])
    sys.exit("front matter が閉じていない")


def cover_range(lines: list[str]) -> tuple[int, int, list[str]] | None:
    """表紙スライド（`_class` に lead を含む最初のスライド）の (開始行, 終了行(排他), クラス一覧)。
    コードブロック内の `---` やディレクティブは数えない。表紙が無ければ None。"""
    fence, start = False, 0
    for i, line in enumerate(lines + ["---"]):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        if line.strip() == "---":
            classes = [c for l in lines[start:i] if (m := CLASS_LINE_RE.match(l.strip())) for c in m.group(1).split()]
            if "lead" in classes:
                return start, i, classes
            start = i + 1
    return None


def apply_cover_event(body: str, name: str) -> tuple[str, str]:
    """表紙が `lead tkt` なら、見出し（`# ... 体験会`）を `# <name> 体験会` にする。(新しい本文, 結果の説明) を返す。"""
    lines = body.split("\n")
    found = cover_range(lines)
    if not found:
        return body, "表紙（_class: lead）が見つからないので、表紙の体験会名は入れていない"
    start, end, classes = found
    if "tkt" not in classes:
        return body, ("表紙が `lead tkt` ではないので、表紙の体験会名は入れていない"
                      "（体験会デッキの表紙は `lead tkt` ＋ `# <体験会名> 体験会`）")
    in_comment = False
    for i in range(start, end):
        # 発表者ノート（HTML コメント）の中の `# ` 行は見出しではないので飛ばす
        if in_comment or lines[i].lstrip().startswith("<!--"):
            in_comment = "-->" not in lines[i]
            continue
        if lines[i].startswith("# "):
            if not COVER_TITLE_RE.match(lines[i]):
                return body, f"表紙の見出し「{lines[i]}」が `# <体験会名> 体験会` の形ではないので、書き換えていない"
            lines[i] = f"# {name} 体験会"
            return "\n".join(lines), f"表紙の見出しを「# {name} 体験会」にした"
    return body, "表紙に見出し（# <体験会名> 体験会）が無いので、表紙の体験会名は入れていない"


def first_heading(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("## "):
            return line
    return ""


def wrap(deck_path: str, opts: dict) -> None:
    deck = Path(deck_path)
    text = deck.read_text(encoding="utf-8")
    event = resolve_event(opts, text)
    opening = apply_event(template_body("opening"), event)
    closing = apply_event(template_body("closing"), event)
    if first_heading(opening) and first_heading(opening) in text:
        print(f"{deck}: 定型スライドは転記済みのようなのでスキップ", file=sys.stderr)
        return
    fm, body = split_front_matter(text)
    body, cover_msg = apply_cover_event(body.strip("\n"), event)
    new = f"{fm}\n{opening}\n---\n\n{body}\n\n---\n\n{closing}"
    deck.write_text(new, encoding="utf-8")
    print(
        f"{deck}: opening を表紙の前に、closing を末尾に転記した。"
        f"体験会名は「{event}」で入れた（{cover_msg}）。"
        "差し替え欄（今後のイベントのお知らせ／○月の主なシンラボ活動の紹介）を最新化すること",
        file=sys.stderr,
    )


def main() -> None:
    args, opts = sys.argv[1:], {}
    for flag in ("--event", "--issue", "--issue-file"):
        if flag in args:
            i = args.index(flag)
            if i + 1 >= len(args):
                sys.exit(__doc__)
            opts[flag[2:].replace("-", "_")] = args[i + 1]
            del args[i : i + 2]
    if len(args) == 2 and args[0] == "print" and args[1] in ("opening", "closing"):
        event = resolve_event(opts) if opts else ""
        sys.stdout.write(apply_event(template_body(args[1]), event))
    elif len(args) == 2 and args[0] == "wrap":
        wrap(args[1], opts)
    elif len(args) == 1 and args[0] == "event" and opts:
        print(resolve_event(opts))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
