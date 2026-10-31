#!/usr/bin/env python3
"""体験会の企画 Issue 本文（下書き）が、デッキ作成（tech-share-deck スキル）に渡せる形になっているかを確かめる。

使い方:
  python3 .claude/skills/taikenkai-plan-issue/scripts/check_plan.py 下書き.md [--today YYYY-MM-DD]

ERROR は直してから起票する。WARN は候補なので、読んで直すか判断する。
終了コードは ERROR があれば 1、なければ 0。

見ること:
- 必須の見出し（基本情報・事前案内・配布物・狙い・タイムテーブル・各パート・スライド構成・Marp 実装メモ・削ってよい）
- 「体験会名」欄（taikenkai_slides.py wrap が読む。空欄・記入例のままだと転記が止まる）
- 発表日（YYYY-MM-DD、月曜か、過去日でないか）
- 各パートの「ひとことスライド文言案」（デッキの見出しになる。空・長すぎ）
- タイムテーブルの合計時間（60 分）と定型 15 分の行
- スライド構成の枚数の合計と、tkb と併用できないクラス
- 骨組みの記入欄（〈〉）・テンプレートの空欄（○分・「」など）の残り
- 前回前提の構成（前回のおさらい など）、回ごとのリポジトリ作成
"""
from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "基本情報",
    "事前案内・配布物",
    "狙い・通しのメッセージ",
    "タイムテーブル",
    "各パート",
    "スライド構成",
    "Marp 実装メモ",
    "削ってよい / 注意する要素",
]
# taikenkai_slides.py の EVENT_ROW_RE と同じ形
EVENT_ROW_RE = re.compile(r"^\|\s*体験会名\s*\|\s*(.*?)\s*\|\s*$", re.M)
DATE_ROW_RE = re.compile(r"^\|\s*発表日\s*\|\s*(.*?)\s*\|\s*$", re.M)
# tkb の見出し（44px）が 1 行に収まる目安。全角 1・半角 0.5 で数える
# （decks/20261102_skills.md の最長「いつも守ることは CLAUDE.md、作業の手順はスキル」が 23）
HEADLINE_MAX = 24
TOTAL_MINUTES = 60
# tkb と併用できない（references/layouts.md「tkb」節）。src は参考スライドだけで使う
TKB_NG = {"trend", "pair", "wide", "split", "refs"}
RECAP_RE = re.compile(r"前回のおさらい|前回までの(流れ|おさらい|内容)|前回の(フォルダ|続き|ファイル)")
NEGATION_RE = re.compile(r"(入れ|置か|使わ|書か|し)ない|前提にしない|不要")
REPO_RE = re.compile(r"(リポジトリ|repo)[^。\n]{0,12}(作る|作成|用意|公開|clone|クローン|fork|フォーク)", re.I)

errors: list[str] = []
warns: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warns.append(msg)


def strip_comments(text: str) -> str:
    """HTML コメントを、行番号がずれないよう改行だけ残して消す。"""
    return re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)


def strip_fences(text: str) -> str:
    """フェンス付きコードブロック（``` / ~~~）の中身を、行番号がずれないよう改行だけ残して消す。
    補足メモに貼った SKILL.md などの `## ` `### ` 行を、見出しと取り違えないため。"""
    out, fence = [], ""
    for line in text.split("\n"):
        m = re.match(r"\s*(`{3,}|~{3,})", line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not line.strip()[len(m.group(1)):]:
                fence = ""
            out.append("")
        elif m:
            fence = m.group(1)
            out.append("")
        else:
            out.append(line)
    return "\n".join(out)


def sections(text: str) -> dict[str, str]:
    """`## 見出し` ごとの本文。"""
    out: dict[str, str] = {}
    parts = re.split(r"(?m)^## +(.+?)\s*$", text)
    for i in range(1, len(parts), 2):
        out[parts[i].strip()] = parts[i + 1]
    return out


def table_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|") or re.fullmatch(r"\|[\s:|-]+\|?", s):
            continue
        rows.append([c.strip() for c in s.strip("|").split("|")])
    return rows


def width(s: str) -> float:
    """見出しの幅の目安。全角 1、半角（ASCII）0.5。"""
    return sum(0.5 if ord(c) < 0x80 else 1 for c in s)


def first_int(cell: str) -> int | None:
    m = re.search(r"\d+", cell)
    return int(m.group(0)) if m else None


def check_basic(sec: str, today: dt.date) -> None:
    m = EVENT_ROW_RE.search(sec)
    value = m.group(1).strip().strip("`") if m else ""
    if not value or value.startswith("例") or "〈" in value:
        err("基本情報：「体験会名」が空欄・記入例のまま（`| 体験会名 | Web技術 |` の形で書く。"
            "デッキ転記の taikenkai_slides.py wrap がここを読む）")
    elif value.endswith("体験会"):
        warn(f"基本情報：体験会名「{value}」の末尾の「体験会」は不要（表紙は「<体験会名> 体験会」になるため二重になる）")

    m = DATE_ROW_RE.search(sec)
    raw = m.group(1).strip() if m else ""
    try:
        day = dt.date.fromisoformat(raw)
    except ValueError:
        err(f"基本情報：発表日「{raw}」が YYYY-MM-DD になっていない")
        return
    if day.weekday() != 0:
        warn(f"基本情報：発表日 {day} は月曜ではない（体験会は月曜 20:00〜21:00 が通常）")
    if day < today:
        warn(f"基本情報：発表日 {day} が過去の日付")


def check_timetable(sec: str) -> None:
    rows = table_rows(sec)
    if len(rows) < 2:
        err("タイムテーブル：表が無い")
        return
    head = rows[0]
    if "目安" not in head:
        err("タイムテーブル：「目安」列が無い")
        return
    i = head.index("目安")
    total, total_row, has_fixed = 0, None, False
    for r in rows[1:]:
        if len(r) <= i:
            continue
        if "合計" in "".join(r):
            total_row = first_int(r[i])
            continue
        if "定型" in "".join(r):
            has_fixed = True
        n = first_int(r[i])
        if n is None:
            err(f"タイムテーブル：「{' | '.join(r)}」の目安が数字になっていない")
        else:
            total += n
    if not has_fixed:
        warn("タイムテーブル：定型（冒頭・末尾）の行が無い（体験会は定型スライドで約 15 分使う）")
    if total != TOTAL_MINUTES:
        warn(f"タイムテーブル：目安の合計が {total} 分（{TOTAL_MINUTES} 分に収める）")
    if total_row is not None and total_row != total:
        warn(f"タイムテーブル：合計行 {total_row} 分と各行の和 {total} 分が合わない")


def check_parts(sec: str) -> None:
    blocks = re.split(r"(?m)^### +(.+?)\s*$", sec)
    if len(blocks) < 3:
        err("各パート：`### n. パート名（n分）` のブロックが無い")
        return
    for i in range(1, len(blocks), 2):
        name, body = blocks[i].strip(), blocks[i + 1]
        if "**話すポイント**" not in body:
            err(f"各パート「{name}」：**話すポイント** が無い（デッキの発表者ノートになる）")
        m = re.search(r"\*\*ひとことスライド文言案\*\*\s*\n>\s*「(.*?)」", body)
        if not m:
            err(f"各パート「{name}」：**ひとことスライド文言案** が `> 「…」` の形で無い（デッキの見出しになる）")
            continue
        line = m.group(1).strip()
        if not line or "〈" in line:
            err(f"各パート「{name}」：ひとことスライド文言案が空")
        elif width(line) > HEADLINE_MAX:
            warn(f"各パート「{name}」：ひとことスライド文言案「{line}」が全角 {width(line):g} 字分"
                 f"（全角 {HEADLINE_MAX} 字分を超えると tkb の見出しが 2 行になりやすい）")


def check_slides(sec: str) -> None:
    rows = table_rows(sec)
    if len(rows) < 2 or "枚数" not in rows[0]:
        err("スライド構成：「枚数」列のある表が無い")
        return
    i = rows[0].index("枚数")
    total, total_row = 0, None
    for r in rows[1:]:
        if len(r) <= i:
            continue
        joined = " | ".join(r)
        if "合計" in joined:
            total_row = first_int(r[i])
            continue
        n = first_int(r[i])
        if n is not None:
            total += n
        is_ref = any(k in r[1] for k in ("参考", "APPENDIX", "出典")) if len(r) > 1 else False
        for cls in re.findall(r"`([^`]+)`", joined):
            words = set(cls.split())
            if words & {"tk"}:
                warn(f"スライド構成「{r[1]}」：`{cls}` の `tk` は定型スライド専用（本編は `tkb`）")
            if not is_ref and "lead" not in words:
                ng = sorted(words & (TKB_NG | {"src"}))
                if ng:
                    warn(f"スライド構成「{r[1]}」：`{cls}` の {', '.join(ng)} は本編（tkb）と併用できない")
    if total_row is not None and total_row != total:
        warn(f"スライド構成：合計 {total_row} 枚と各行の和 {total} 枚が合わない（デッキ作成時は内訳が優先される）")


def check_text(text: str) -> None:
    for no, line in enumerate(text.splitlines(), 1):
        if "〈" in line and "〉" in line:
            err(f"{no} 行目：骨組みの記入欄（〈〉）が残っている：{line.strip()[:60]}")
        for pat, what in (("○○", "○○"), ("○分", "○分"), ("YYYY-MM-DD", "YYYY-MM-DD"), ("「」", "「」")):
            if pat in line:
                warn(f"{no} 行目：テンプレートの空欄（{what}）が残っている：{line.strip()[:60]}")
        if RECAP_RE.search(line) and not NEGATION_RE.search(line):
            warn(f"{no} 行目：前回前提の構成に見える（単発参加者が多いので入れない）：{line.strip()[:60]}")
        if REPO_RE.search(line) and not re.search(r"作らない|不要|使わない", line):
            warn(f"{no} 行目：回ごとのリポジトリを用意する前提に見える（配布はファイルを Zoom で共有）：{line.strip()[:60]}")


def main() -> None:
    args = sys.argv[1:]
    today = dt.date.today()
    if "--today" in args:
        j = args.index("--today")
        today = dt.date.fromisoformat(args[j + 1])
        del args[j:j + 2]
    if len(args) != 1:
        sys.exit(__doc__)
    raw = Path(args[0]).read_text(encoding="utf-8")
    text = strip_comments(raw)
    secs = sections(strip_fences(text))

    for name in REQUIRED_SECTIONS:
        if name not in secs:
            err(f"見出し「## {name}」が無い")
    if "基本情報" in secs:
        check_basic(secs["基本情報"], today)
    if "タイムテーブル" in secs:
        check_timetable(secs["タイムテーブル"])
    if "各パート" in secs:
        check_parts(secs["各パート"])
    if "スライド構成" in secs:
        check_slides(secs["スライド構成"])
    check_text(text)

    for m in errors:
        print(f"ERROR {m}")
    for m in warns:
        print(f"WARN  {m}")
    print(f"--- ERROR {len(errors)} / WARN {len(warns)}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
