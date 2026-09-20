#!/usr/bin/env python3
"""Report literal occurrences of configured terms in UTF-8 text.

語と記号の表は ../references/ に置いてある。出どころは
~/.codex/skills/avoid-ai-cliches-ja で、その写し。
記号の表からは → を外してある（理由は SKILL.md）。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_TERMS = (
    Path(__file__).resolve().parent.parent
    / "references"
    / "forbidden-terms.txt"
)
DEFAULT_SYMBOLS = (
    Path(__file__).resolve().parent.parent
    / "references"
    / "discouraged-symbols.txt"
)


def load_terms(path: Path) -> list[str]:
    terms = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    return list(dict.fromkeys(term for term in terms if term))


def iter_matches(text: str, terms: list[str]):
    for term in terms:
        start = 0
        while True:
            index = text.find(term, start)
            if index < 0:
                break
            line = text.count("\n", 0, index) + 1
            previous_newline = text.rfind("\n", 0, index)
            column = index - previous_newline
            yield index, line, column, term
            start = index + len(term)


def check_text(
    text: str,
    label: str,
    terms: list[str],
    symbols: list[str],
) -> int:
    matches = [
        (*match, "disallowed term") for match in iter_matches(text, terms)
    ]
    matches.extend(
        (*match, "discouraged symbol") for match in iter_matches(text, symbols)
    )
    matches.sort(key=lambda item: item[0])
    for _, line, column, item, category in matches:
        print(f"{label}:{line}:{column}: {category}: {item}")
    return len(matches)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check UTF-8 text for configured literal terms."
    )
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--stdin", action="store_true", help="check standard input")
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--symbols", type=Path, default=DEFAULT_SYMBOLS)
    parser.add_argument(
        "--skip-symbols",
        action="store_true",
        help="check terms without checking punctuation",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.stdin and args.files:
        print("--stdin cannot be combined with file paths", file=sys.stderr)
        return 2
    if not args.stdin and not args.files:
        print("provide a file path or --stdin", file=sys.stderr)
        return 2

    try:
        terms = load_terms(args.terms)
        if not terms:
            print(f"term list is empty: {args.terms}", file=sys.stderr)
            return 2
        symbols = [] if args.skip_symbols else load_terms(args.symbols)
        if not args.skip_symbols and not symbols:
            print(f"symbol list is empty: {args.symbols}", file=sys.stderr)
            return 2

        if args.stdin:
            count = check_text(sys.stdin.read(), "<stdin>", terms, symbols)
        else:
            count = 0
            for path in args.files:
                count += check_text(
                    path.read_text(encoding="utf-8"), str(path), terms, symbols
                )
    except (OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        return 2

    return 1 if count else 0


if __name__ == "__main__":
    raise SystemExit(main())
