#!/usr/bin/env python3
"""スライド数と本文の文字数を測る。

    python3 slide-stats.py <deck>.md [--over N]

本文の文字数は、発表者ノート・コードブロック・HTMLタグ・<Overview> の props を
除いたもの。スライドに「読ませている」量の目安になる。

コードフェンスの中にも `---` が出る（.astro の Component script など）ので、
フェンスの内外を追いながら分割する。フロントマターの `---` も飛ばす。
"""
import re
import statistics
import sys


FENCE = re.compile(r"^(`{3,}|~{3,})(.*)$")


def split_slides(src: str) -> list[str]:
    """`---` でスライドを分ける。ただしコードフェンスの中は無視する。

    フェンスは開いた記号の長さを覚えて、同じ記号で同じ長さ以上・情報文字列なし
    の行でだけ閉じる（CommonMark と同じ規則）。````md magic-move の中に ```astro
    が入る書き方があり、単純な toggle だと内側で閉じたと誤判定して、.astro の
    frontmatter の `---` をスライド区切りに数えてしまう。
    """
    lines = src.split("\n")
    slides, cur = [], []
    fence_char, fence_len = None, 0
    i = 1  # 先頭のフロントマターを飛ばす
    while i < len(lines) and lines[i] != "---":
        i += 1
    i += 1
    while i < len(lines):
        line = lines[i]
        m = FENCE.match(line)
        if m:
            marker, info = m.group(1), m.group(2).strip()
            if fence_char is None:
                fence_char, fence_len = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_len and not info:
                fence_char, fence_len = None, 0
        fence = fence_char is not None
        if not fence and line == "---":
            slides.append("\n".join(cur))
            cur = []
            # 区切りの直後がスライド frontmatter ならまとめて飛ばす
            j, buf = i + 1, []
            while j < len(lines) and lines[j] != "---" and not FENCE.match(lines[j]):
                buf.append(lines[j])
                j += 1
            is_fm = (
                j < len(lines)
                and lines[j] == "---"
                and buf
                and all(re.match(r"^[\w-]+:|^\s+", b) or b == "" for b in buf)
            )
            i = j + 1 if is_fm else i + 1
            continue
        cur.append(line)
        i += 1
    slides.append("\n".join(cur))
    return slides


def body_chars(slide: str) -> int:
    s = re.sub(r"<!--.*?-->", "", slide, flags=re.S)      # 発表者ノート
    s = re.sub(r"```.*?```", "", s, flags=re.S)           # コード
    s = re.sub(r"<Overview[\s\S]*?/>", "", s)             # 図の props
    s = re.sub(r"<[^>]+>", "", s)                         # HTMLタグ
    return len(re.sub(r"\s+", "", s))


def title_of(slide: str) -> str:
    m = re.search(r"^#+\s*(.+)$", slide, re.M)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    if "<Overview" in slide:
        return "（全体図）"
    m = re.search(r">([^<>\n]{3,40})<", slide)
    return f"（図）{m.group(1)}" if m else ""


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    over = 180
    if "--over" in sys.argv:
        over = int(sys.argv[sys.argv.index("--over") + 1])

    slides = split_slides(open(path, encoding="utf-8").read())
    counts = [body_chars(s) for s in slides]
    no_notes = [n for n, s in enumerate(slides, 1) if "<!--" not in s]

    print(f"総スライド数 : {len(slides)}")
    print(f"本文の中央値 : {statistics.median(counts):.0f}字  平均 {statistics.mean(counts):.0f}字")
    print(f"{over}字超      : {sum(1 for c in counts if c > over)}枚")
    print(f"発表者ノート無し: {no_notes if no_notes else 'なし'}")

    heavy = sorted(((c, n) for n, c in enumerate(counts, 1) if c > over), reverse=True)
    if heavy:
        print(f"\n--- {over}字を超えたスライド ---")
        for c, n in heavy:
            print(f"{n:3d}  {c:4d}字  {title_of(slides[n - 1])[:44]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
