#!/usr/bin/env python3
"""Tech Share の Marp デッキが CLAUDE.md の規約を満たすかを検査する。

使い方（リポジトリ直下で実行）:
  python3 .claude/skills/tech-share-deck/scripts/check_deck.py decks/YYYYMMDD_topic.md [--taikenkai] [--issue-file 本文.md]

--taikenkai: 企画 Issue に `体験会` ラベルが付いているとき指定する。定型スライドの転記漏れを ERROR にする。
また、表紙が `lead tkt`（`# <体験会名> 体験会` ＋ `<p class="sub">`）でない、本編スライドに `tkb` が無い、
`tkb` と併用すると崩れるクラスを使っている、`tkb` で項目が多すぎる、を WARN にする。
指定しなくても、デッキに定型スライドが入っていれば転記内容を検査する。
定型スライドと表紙（`lead tkt`）の体験会名は、表紙の企画 Issue の「体験会名」欄と照合する（Issue 本文は gh で取得。
gh が無い環境では Issue 本文を保存したファイルを --issue-file で渡す。どちらも無ければ WARN で照合を飛ばす）。

ERROR は直すべき規約違反、WARN は目視で判断する候補。はみ出しはこのスクリプトでは分からないので、
PNG 書き出しで必ず確認すること。終了コードは ERROR があれば 1。
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from taikenkai_slides import (  # noqa: E402
    COVER_TITLE_RE, EVENT_DEFAULT, EVENT_SLIDE_RE, ISSUE_URL_RE, REPO, event_from_issue_body, template_body,
)
import subprocess  # noqa: E402

ISSUE_URL = re.compile(r"企画 Issue：https://github\.com/Singuralitylabs/tech-share/issues/\d+")
CLASS_RE = re.compile(r"<!--\s*_class:\s*([^>]*?)\s*-->")
DIRECTIVE_RE = re.compile(r"^<!--\s*_?\w+:.*-->$")
# CLAUDE.md「日本語で **太字** が効かないパターン」の洗い出し用 grep から、直後が句読点・約物のもの（問題ない）を除いた版
BOLD_RE = re.compile(r"[\"」』）]\*\*[^ 　、。，．！？：；!?:;）」』\s]")
KEYOP_RE = re.compile(r"\b(Shift|Ctrl|Cmd|Command|Alt|Option|Esc|Enter|Tab)\s*\+", re.I)
# tkb（体験会デッキの本編）と併用すると崩れる／未対応のクラス（references/layouts.md「tkb」節）
TKB_BROKEN = ("trend", "pair", "split", "refs", "src", "lead", "tk")
# tkb を付けずにそのまま使う本編スライド（APPENDIX の出典・注記）
TKB_EXEMPT = ("src", "refs", "split")
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


def template_pattern(tmpl: str) -> re.Pattern:
    """定型スライド1枚と照合する正規表現。体験会名の差し替え欄は、1枚の中で同じ名前なら任意の名前を許す。"""
    if not EVENT_SLIDE_RE.search(tmpl):
        return re.compile(re.escape(tmpl))
    parts = [re.escape(p) for p in tmpl.split(EVENT_DEFAULT)]
    out = parts[0]
    for k, p in enumerate(parts[1:]):
        out += (r"(?P<ev>[^\n]+?)" if k == 0 else r"(?P=ev)") + p
    return re.compile(out)


def same(text: str, tmpl: str, events: list[str] | None = None) -> bool:
    """定型スライド1枚と一致するか。events を渡すと、差し替え欄の体験会名をそこへ集める（スライド間の一致検査用）。"""
    m = template_pattern(tmpl).fullmatch(text)
    if m and events is not None and "ev" in m.groupdict():
        events.append(m.group("ev"))
    return bool(m)


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


def issue_event(deck_text: str, issue_file: str) -> tuple[str, str]:
    """企画 Issue の「体験会名」欄を (値, 取得元) で返す。値が取れないときは ("", 照合できない理由)。"""
    if issue_file:
        value = event_from_issue_body(Path(issue_file).read_text(encoding="utf-8"))
        return (value, issue_file) if value else ("", f"{issue_file} の「体験会名」欄が空")
    m = ISSUE_URL_RE.search(deck_text)
    if not m:
        return "", "表紙に企画 Issue の URL がない"
    try:
        body = subprocess.run(
            ["gh", "issue", "view", m.group(1), "--repo", REPO, "--json", "body", "-q", ".body"],
            capture_output=True, text=True, check=True, timeout=30,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return "", f"企画 Issue #{m.group(1)} を gh で取得できない"
    value = event_from_issue_body(body)
    return (value, f"企画 Issue #{m.group(1)}") if value else ("", f"企画 Issue #{m.group(1)} の「体験会名」欄が空")


def check_taikenkai(slides: list[Slide], required: bool, deck_text: str = "", issue_file: str = "") -> set[int]:
    """定型スライドを検査し、定型として扱ったスライドの index を返す。"""
    opening, closing = template_slides("opening"), template_slides("closing")
    texts = [norm(s.text) for s in slides]
    closing_head = Slide(0, closing[0].splitlines()).heading()
    present = any(same(t, opening[0]) for t in texts[:3]) or any(
        same(s.heading(), closing_head) for s in slides[-len(closing):]
    )
    if not present:
        if required:
            err("体験会デッキなのに定型スライド（templates/taikenkai-*.md）が転記されていない")
        return set()

    used: set[int] = set()
    events: list[str] = []  # アンケート・ご支援スライドの体験会名。opening・closing を通して1種類であること
    # opening：表紙の直前に全枚・同順・同文
    lead_idx = next((i for i, s in enumerate(slides) if "lead" in " ".join(s.classes()).split()), None)
    if lead_idx is None:
        lead_idx = len(opening)
    if lead_idx != len(opening):
        err(f"表紙（_class: lead）の前のスライドが {lead_idx} 枚。opening 定型は {len(opening)} 枚（全枚を表紙の直前に置く）")
    for j, t in enumerate(opening):
        if j < lead_idx and same(texts[j], t, events):
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
            ok = same(texts[k], t, events)
        if ok:
            used.add(k)
        else:
            err(f"L{s.start}: closing 定型 {j + 1} 枚目（{tmpl_head[3:]}）が templates/taikenkai-closing.md と一致しない（文言改変・合体・欠落・`---` 漏れ）")
    cover = check_cover(slides[lead_idx], required) if lead_idx < len(slides) else None
    if len(set(events)) > 1:
        err(f"体験会名が不一致：{sorted(set(events))}（アンケート・ご支援スライドの体験会名は opening・closing を通して同じ名前にそろえる）")
    elif events and cover and cover[1] != events[0]:
        err(f"L{cover[0]}: 表紙の体験会名「{cover[1]}」が定型スライドの「{events[0]}」と違う（表紙は `# <体験会名> 体験会`。同じ名前にそろえる）")
    elif events or cover:
        name = events[0] if events else cover[1]
        expected, where = issue_event(deck_text, issue_file)
        if expected and expected != name:
            err(f"体験会名「{name}」が {where} の「体験会名」欄「{expected}」と違う（`taikenkai_slides.py wrap` で入れ直すか、表紙・定型スライドを直す）")
        elif not expected:
            warn(f"体験会名「{name}」を企画 Issue と照合できなかった（{where}）。--issue-file で Issue 本文を渡すと照合する")
    if required:
        check_tkb(slides[lead_idx + 1:max(base, lead_idx + 1)])
    return used


def check_cover(lead: Slide, required: bool) -> tuple[int, str] | None:
    """体験会デッキの表紙（lead tkt）を検査し、見出しから読んだ (行番号, 体験会名) を返す。読めなければ None。"""
    names = " ".join(lead.classes()).split()
    if "tkt" not in names:
        if required:
            warn(f"L{lead.start}: 体験会デッキの表紙が `lead tkt` ではない（`<!-- _class: lead tkt -->` ＋ `# <体験会名> 体験会` ＋ `<p class=\"sub\">その回のテーマ</p>`）")
        return None
    visible = lead.visible_lines()
    h1 = next((l for l in visible if l.startswith("# ")), "")
    ln = lead.start + lead.lines.index(h1) if h1 else lead.start
    m = COVER_TITLE_RE.match(h1)
    if not m or not m.group(1):
        warn(f"L{ln}: 表紙（lead tkt）の見出しが `# <体験会名> 体験会` の形ではない: {h1 or '（見出しなし）'}")
        m = None
    if not any('class="sub"' in l for l in visible):
        warn(f"L{lead.start}: 表紙（lead tkt）に `<p class=\"sub\">その回のテーマ</p>` がない")
    if any('class="kicker"' in l for l in visible):
        warn(f"L{lead.start}: 表紙（lead tkt）に kicker がある。体験会デッキの表紙には日付の kicker を付けない")
    return (ln, m.group(1)) if m else None


def check_tkb(main: list[Slide]) -> None:
    """体験会デッキの本編スライド（表紙と closing 定型の間）が tkb で書かれているか、tkb で入りきる量かを見る。"""
    missing = []
    for s in main:
        names = " ".join(s.classes()).split()
        if "tkb" not in names:
            if not any(c in names for c in TKB_EXEMPT):
                missing.append(f"L{s.start}")
            continue
        broken = [c for c in TKB_BROKEN if c in names]
        if broken:
            warn(f"L{s.start}: tkb と {' / '.join(broken)} は併用できない（レイアウトが崩れる）。references/layouts.md の tkb 節を参照")
        vis = s.visible_lines()
        top = sum(1 for l in vis if re.match(r"^([-*]|\d+\.) ", l))
        if "grid" in names:
            cards, subs = [], 0
            for l in vis:
                if re.match(r"^[-*] ", l):
                    cards.append(0)
                elif cards and re.match(r"^\s+[-*] ", l):
                    cards[-1] += 1
            if len(cards) == 4 and max(cards) > 2:
                warn(f"L{s.start}: tkb grid で 4 枚のカードに説明が {max(cards)} 行ある（4 枚なら各 2 行まで。3 行以上は 3 枚にする）")
            elif len(cards) <= 3 and cards and max(cards) > 3:
                warn(f"L{s.start}: tkb grid のカードに説明が {max(cards)} 行ある（3 枚なら各 3 行まで）")
        elif "flow" in names:
            if top > 4:
                warn(f"L{s.start}: tkb flow のステップが {top} 個（4 個まで。5 個だとステップ名が折り返す）")
        elif "ba" in names:
            rows = sum(1 for l in vis if l.startswith("|")) - 2
            if rows > 4 or (rows == 4 and top > 1):
                warn(f"L{s.start}: tkb ba が表 {rows} 行＋補足 {top} 個（表 4 行＋補足 1 個まで）")
        elif "dense" in names:
            fences = sum(1 for l in vis if l.lstrip().startswith("```")) // 2
            if fences > 3:
                warn(f"L{s.start}: tkb dense にコードブロックが {fences} 個（ラベル付きで 3 個まで）")
        elif not names or names == ["tkb"] or "center" in names:
            quotes = sum(1 for l in vis if l.startswith(">"))
            if top + quotes > 6:
                warn(f"L{s.start}: tkb の本文が箇条書き {top} 個＋引用 {quotes} 行（合わせて 6 つまで。箇条書き 5 個＋引用 1 行が上限）")
    if missing:
        warn(f"体験会デッキの本編スライドに `tkb` が無い：{', '.join(missing)}（本編の各スライドに `<!-- _class: tkb ... -->` を付ける。APPENDIX の src / refs split は除く）")


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
    argv = sys.argv[1:]
    if "--issue-file" in argv[:-1]:
        i = argv.index("--issue-file")
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    path = Path(args[0])
    lines = path.read_text(encoding="utf-8").splitlines()
    body_start = check_front_matter(lines, path)
    slides = split_slides(lines[body_start:], body_start)
    issue_file = sys.argv[sys.argv.index("--issue-file") + 1] if "--issue-file" in sys.argv[:-1] else ""
    tk = check_taikenkai(slides, "--taikenkai" in sys.argv, "\n".join(lines), issue_file)
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
