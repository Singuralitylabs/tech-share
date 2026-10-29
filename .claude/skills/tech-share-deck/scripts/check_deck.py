#!/usr/bin/env python3
"""Tech Share の Marp デッキが CLAUDE.md の規約を満たすかを検査する。

使い方（リポジトリ直下で実行）:
  python3 .claude/skills/tech-share-deck/scripts/check_deck.py decks/YYYYMMDD_topic.md [--taikenkai]

--taikenkai: 企画 Issue に `体験会` ラベルが付いているとき指定する。定型スライドの転記漏れを ERROR にする。
指定しなくても、デッキに定型スライドが入っていれば転記内容を検査する。

ERROR は直すべき規約違反、WARN は目視で判断する候補。はみ出しはこのスクリプトでは分からないので、
PNG 書き出しで必ず確認すること。終了コードは ERROR があれば 1。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from taikenkai_slides import template_body  # noqa: E402

ISSUE_URL = re.compile(r"企画 Issue：https://github\.com/Singuralitylabs/tech-share/issues/\d+")
CLASS_RE = re.compile(r"<!--\s*_class:\s*([^>]*?)\s*-->")
DIRECTIVE_RE = re.compile(r"^<!--\s*_?\w+:.*-->$")
# CLAUDE.md「日本語で **太字** が効かないパターン」の洗い出し用 grep から、直後が句読点・約物のもの（問題ない）を除いた版
BOLD_RE = re.compile(r"[\"」』）]\*\*[^ 　、。，．！？：；!?:;）」』\s]")
KEYOP_RE = re.compile(r"\b(Shift|Ctrl|Cmd|Command|Alt|Option|Esc|Enter|Tab)\s*\+", re.I)
REPLACEABLE = (re.compile(r"^## 今後のイベントのお知らせ$"), re.compile(r"^## (\d{1,2}|○)月の主なシンラボ活動の紹介$"))

errors: list[str] = []
warns: list[str] = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warns.append(msg)


class Slide:
    def __init__(self, start: int, lines: list[str]):
        self.start = start  # 1-indexed line number of first line
        self.lines = lines

    @property
    def text(self) -> str:
        return "\n".join(self.lines).strip("\n")

    def heading(self) -> str:
        for l in self.lines:
            if re.match(r"^#{1,2} ", l):
                return l
        return ""

    def visible_lines(self) -> list[str]:
        """発表者ノート（HTML コメント）を除いた、スライドに描画される行。"""
        out, in_comment = [], False
        for l in self.lines:
            if not in_comment and l.lstrip().startswith("<!--"):
                in_comment = "-->" not in l
                continue
            if in_comment:
                in_comment = "-->" not in l
                continue
            out.append(l)
        return out

    def classes(self) -> list[str]:
        return CLASS_RE.findall(self.text)


def split_slides(lines: list[str], offset: int) -> list[Slide]:
    slides, cur, start, fence = [], [], offset + 1, False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
        if line.strip() == "---" and not fence:
            slides.append(Slide(start, cur))
            cur, start = [], offset + i + 2
        else:
            cur.append(line)
    slides.append(Slide(start, cur))
    return [s for s in slides if s.text.strip()]


def norm(text: str) -> str:
    return "\n".join(l.rstrip() for l in text.strip("\n").splitlines())


def template_slides(kind: str) -> list[str]:
    body = template_body(kind)
    return [norm(s.text) for s in split_slides(body.splitlines(), 0)]


def check_front_matter(lines: list[str], path: Path) -> int:
    if not lines or lines[0].strip() != "---":
        err("front matter がない（1行目が --- ではない）")
        return 0
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        err("front matter が閉じていない")
        return 0
    fm = "\n".join(lines[1:end])
    if not re.search(r"^theme:\s*singularity\s*$", fm, re.M):
        err("front matter に `theme: singularity` がない")
    if not re.search(r"^marp:\s*true\s*$", fm, re.M):
        err("front matter に `marp: true` がない")
    for key in ("size", "paginate", "lang", "title", "description", "author", "footer"):
        if not re.search(rf"^{key}:", fm, re.M):
            warn(f"front matter に `{key}:` がない（既存デッキは size/paginate/lang/title/description/author/footer を揃えている）")
    if "<style" in "\n".join(lines):
        err("インライン <style> がある。デザインは themes/singularity.css 側で持つ")
    if not re.match(r"^\d{8}_[\w-]+\.md$", path.name) or path.name.endswith(".gslides.md"):
        warn(f"ファイル名 {path.name} が decks/YYYYMMDD_<topic>.md の形ではない")
    return end + 1


def check_taikenkai(slides: list[Slide], required: bool) -> set[int]:
    """定型スライドを検査し、定型として扱ったスライドの index を返す。"""
    opening, closing = template_slides("opening"), template_slides("closing")
    texts = [norm(s.text) for s in slides]
    present = any(t == opening[0] for t in texts[:3]) or any(
        s.heading() == Slide(0, closing[0].splitlines()).heading() for s in slides[-len(closing):]
    )
    if not present:
        if required:
            err("体験会デッキなのに定型スライド（templates/taikenkai-*.md）が転記されていない")
        return set()

    used: set[int] = set()
    # opening：表紙の直前に全枚・同順・同文
    lead_idx = next((i for i, s in enumerate(slides) if "lead" in " ".join(s.classes()).split()), None)
    if lead_idx is None:
        lead_idx = len(opening)
    if lead_idx != len(opening):
        err(f"表紙（_class: lead）の前のスライドが {lead_idx} 枚。opening 定型は {len(opening)} 枚（全枚を表紙の直前に置く）")
    for j, t in enumerate(opening):
        if j < lead_idx and texts[j] == t:
            used.add(j)
        else:
            s = slides[j] if j < len(slides) else None
            where = f"L{s.start}" if s else "末尾"
            err(f"{where}: opening 定型 {j + 1} 枚目が templates/taikenkai-opening.md と一致しない（文言改変・合体・欠落・`---` 漏れ）")

    # closing：デッキの最後に全枚・同順・同文（差し替え欄2枚は見出しの型とディレクティブだけ確認）
    base = len(slides) - len(closing)
    for j, t in enumerate(closing):
        k = base + j
        if k < 0 or k < lead_idx:
            err(f"closing 定型 {j + 1} 枚目がデッキ末尾に無い")
            continue
        s, tmpl = slides[k], Slide(0, t.splitlines())
        tmpl_head = tmpl.heading()
        replaceable = next((p for p in REPLACEABLE if p.match(tmpl_head)), None)
        if replaceable:
            ok = bool(replaceable.match(s.heading())) and all(
                l in s.lines for l in tmpl.lines if DIRECTIVE_RE.match(l.strip())
            )
            if ok and texts[k] == t:
                warn(f"L{s.start}: 差し替え欄「{s.heading()[3:]}」がテンプレートのまま。最新の内容に更新したか確認する")
        else:
            ok = texts[k] == t
        if ok:
            used.add(k)
        else:
            err(f"L{s.start}: closing 定型 {j + 1} 枚目（{tmpl_head[3:]}）が templates/taikenkai-closing.md と一致しない（文言改変・合体・欠落・`---` 漏れ）")
    return used


def check_slides(slides: list[Slide], taikenkai_idx: set[int]) -> None:
    leads = [s for s in slides if "lead" in " ".join(s.classes()).split()]
    if not leads:
        err("表紙スライド（<!-- _class: lead -->）がない")
    else:
        lead = leads[0]
        comments = re.findall(r"<!--(.*?)-->", lead.text, re.S)
        notes = [c.strip() for c in comments if not DIRECTIVE_RE.match(f"<!--{c}-->".strip())]
        if not notes or not ISSUE_URL.match(notes[0].splitlines()[0]):
            err(f"L{lead.start}: 表紙のコメント先頭に `企画 Issue：https://github.com/Singuralitylabs/tech-share/issues/N` がない")

    for i, s in enumerate(slides):
        cls = s.classes()
        if len(cls) > 1:
            err(f"L{s.start}: `_class` が {len(cls)} 行ある（後勝ちで {cls[:-1]} が消える）。1行に半角スペース区切りでまとめる")
        names = " ".join(cls).split()
        if "refs" in names and "src" in names:
            warn(f"L{s.start}: refs と src を併用している（font-size が 18px になる）。出典は src 単独で")
        if i in taikenkai_idx:
            continue
        if "_paginate: false" in s.text and "lead" not in names:
            warn(f"L{s.start}: `_paginate: false` は番号を隠すだけでカウントは進む。カウントからも外すなら `skip`")
        if not s.heading() and "lead" not in names:
            warn(f"L{s.start}: 見出し（## ...）がない")
        # 発表者ノート：ディレクティブ以外のコメントがあるか
        comments = re.findall(r"<!--(.*?)-->", s.text, re.S)
        if not any(not DIRECTIVE_RE.match(f"<!--{c}-->".strip()) for c in comments):
            warn(f"L{s.start}: 発表者ノート（スライド末尾の <!-- ... -->）がない「{s.heading()[3:]}」")
        if "split" in names:
            items = sum(1 for l in s.visible_lines() if re.match(r"^\s*([-*]|\d+\.) ", l))
            if items > 5:
                warn(f"L{s.start}: split で項目が {items} 個。右パネルで本文幅が半分になるので、はみ出しを PNG で確認する")
        if "grid" in names:
            top = sum(1 for l in s.visible_lines() if re.match(r"^[-*] ", l))
            if top > 4:
                warn(f"L{s.start}: grid のカードが {top} 枚（2×2 か横3枚が前提）")
        if "pair" in names and 'class="fig"' not in s.text:
            warn(f"L{s.start}: pair なのに <p class=\"fig\"> がない")

        fence = False
        visible = set(map(id, s.visible_lines()))
        for off, line in enumerate(s.lines):
            if id(line) not in visible:
                continue
            if line.lstrip().startswith("```"):
                fence = not fence
                continue
            ln = s.start + off
            if fence:
                if KEYOP_RE.search(line):
                    warn(f"L{ln}: コードブロック内にキー操作らしき記述。キー操作は引用（>）＋インラインコードで書く: {line.strip()}")
                continue
            if BOLD_RE.search(line):
                warn(f"L{ln}: 太字が効かない可能性（閉じ ** の直前が約物・直後が文字）: {line.strip()}")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    path = Path(args[0])
    lines = path.read_text(encoding="utf-8").splitlines()
    body_start = check_front_matter(lines, path)
    slides = split_slides(lines[body_start:], body_start)
    tk = check_taikenkai(slides, "--taikenkai" in sys.argv)
    check_slides(slides, tk)

    print(f"{path}: {len(slides)} 枚（うち体験会定型 {len(tk)} 枚）")
    for m in errors:
        print(f"ERROR {m}")
    for m in warns:
        print(f"WARN  {m}")
    if not errors and not warns:
        print("OK")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
