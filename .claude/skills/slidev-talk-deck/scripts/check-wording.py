#!/usr/bin/env python3
"""Check prose in Slidev Markdown, source documents, and Vue components.

語と記号の表は ../references/ に置いてある。出どころは
~/.codex/skills/avoid-ai-cliches-ja で、その写し。
記号の表からは → を外してある（理由は SKILL.md）。
"""

from __future__ import annotations

import argparse
import glob
import re
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
DEFAULT_COMPOUNDS = DEFAULT_TERMS.with_name("allowed-you-compounds.txt")

# Keep offsets intact so findings always refer to the original source file.
def blank(text: str) -> str:
    return re.sub(r"[^\n]", " ", text)


JS_TOKEN = re.compile(
    r'''//[^\n]*|/\*[\s\S]*?\*/|'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*"|`(?:\\.|[^`\\])*`'''
)


def display_strings(source: str) -> str:
    """Keep JS string values, excluding comments and object property names.

    This is a lexical check, not runtime data-flow analysis: string values in
    script blocks and Vue expressions are possible display text. Identifiers
    and code outside strings are not prose.
    """
    result = list(blank(source))
    for match in JS_TOKEN.finditer(source):
        token = match.group()
        if token.startswith(("//", "/*")):
            continue
        # A quoted object key is an identifier, not a displayed value.
        after = source[match.end():].lstrip()
        before = source[:match.start()].rstrip()
        if after.startswith(":") and (not before or before[-1] in "{,"):
            continue
        value = token[1:-1]
        if token.startswith("`"):
            value = re.sub(r"\$\{[^{}]*\}", lambda m: blank(m.group()), value)
        result[match.start() + 1:match.end() - 1] = value
    return "".join(result)


TAG = re.compile(r'''</?[A-Za-z][\w:.-]*(?:[^>"']|"[^"]*"|'[^']*')*>''')
ATTRIBUTE = re.compile(r'''([^\s=<>]+)\s*=\s*("[^"]*"|'[^']*'|[^\s=<>`]+)''')
TEXT_ATTRIBUTES = {"alt", "title", "aria-label", "aria-description", "placeholder", "label", "description", "caption"}
DISPLAY_PROPS = {"labels", "subnotes", "annotate", "roles", "edgeLabels"}
CODE_ATTRIBUTES = {"class", "id", "style", "src", "href", "key", "ref", "is", "to"}


def tag_prose(match: re.Match) -> str:
    tag = match.group()
    result = list(blank(tag))
    for attr in ATTRIBUTE.finditer(tag):
        name, raw = attr.groups()
        quoted = raw.startswith(("'", '"'))
        value = raw[1:-1] if quoted else raw
        start = attr.start(2) + int(quoted)
        binding = name.startswith((":", "v-bind:")) or name in {"v-text", "v-html"}
        plain_name = name.removeprefix("v-bind:").removeprefix(":")
        if plain_name in CODE_ATTRIBUTES:
            continue
        if binding:
            # Component props may carry diagram labels as object values.
            value = display_strings(value)
        elif plain_name not in TEXT_ATTRIBUTES | DISPLAY_PROPS:
            continue
        result[start:start + len(value)] = value
    return "".join(result)


def prose_only(source: str) -> str:
    """Mask code and destinations while retaining notes and displayed prose."""
    lines = source.splitlines(keepends=True)
    fence_char, fence_length = "", 0
    for index, line in enumerate(lines):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence_char:
            lines[index] = blank(line)
            if match and match[1][0] == fence_char and len(match[1]) >= fence_length and not match[2].strip():
                fence_char = ""
        elif match:
            fence_char, fence_length = match[1][0], len(match[1])
            lines[index] = blank(line)
    text = "".join(lines)
    # Handwritten code examples and styles are code as well.
    text = re.sub(r"<(pre|code|style)\b[^>]*>[\s\S]*?</\1\s*>", lambda m: blank(m.group()), text, flags=re.I)
    # Save script strings before applying HTML and Markdown rules.
    scripts = []
    def script(match):
        scripts.append((match.start(1), display_strings(match[1])))
        return blank(match.group())
    text = re.sub(r"<script\b[^>]*>([\s\S]*?)</script\s*>", script, text, flags=re.I)
    # Protect Vue strings from Markdown's inline-code rule, including template
    # literals. The alternation still masks actual Markdown inline examples.
    token = re.compile(TAG.pattern + r"|\{\{[\s\S]*?\}\}|(`+)(?!`)([\s\S]*?)(?<!`)\1(?!`)")
    def markup(match):
        value = match.group()
        if value.startswith("<"):
            return tag_prose(match)
        if value.startswith("{{"):
            return "  " + display_strings(value[2:-2]) + "  "
        return blank(value)
    # Note bodies remain checkable; only their delimiters are masked.
    text = text.replace("<!--", "    ").replace("-->", "   ")
    text = token.sub(markup, text)
    # Markdown destinations and reference definitions do not contain prose.
    text = re.sub(r"(?<=\]\()([^\s)]*)(?=[\s)])", lambda m: blank(m.group()), text)
    text = re.sub(r"(?m)^(\s{0,3}\[[^\]\n]+\]:\s*)(\S+)", lambda m: m[1] + blank(m[2]), text)
    chars = list(text)
    for start, value in scripts:
        chars[start:start + len(value)] = value
    text = "".join(chars)
    # Preserve punctuation following bare URLs and file paths as prose.
    destinations = re.compile(
        r'''https?://[^\s<>"'`、。）」]+'''
        r'''|(?<![\w])(?:~?/|\.{1,2}/|[\w.@-]+/)[\w./@%+~#?=&-]+'''
        r'''|(?<![\w])[\w.@-]+\.(?:md|vue|ts|tsx|js|jsx|mjs|cjs|json|astro|rs|css|png|svg)\b'''
    )
    text = destinations.sub(lambda m: blank(m.group()), text)
    return text


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
    compounds: list[str] | None = None,
) -> int:
    text = prose_only(text)
    matches = [
        (*match, "disallowed term") for match in iter_matches(text, terms)
    ]
    matches.extend(
        (*match, "discouraged symbol") for match in iter_matches(text, symbols)
    )
    allowed = set()
    for word in compounds if compounds is not None else load_terms(DEFAULT_COMPOUNDS):
        for index, _, _, _ in iter_matches(text, [word]):
            allowed.update(range(index, index + len(word)))
    matches.extend(
        (*match, "review purpose suffix or unregistered compound")
        for match in iter_matches(text, ["用"]) if match[0] not in allowed
    )
    matches.sort(key=lambda item: item[0])
    for _, line, column, item, category in matches:
        print(f"{label}:{line}:{column}: {category}: {item}")
    return len(matches)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check prose for prohibited terms and unregistered 用 expressions."
    )
    parser.add_argument("files", nargs="*", help="file paths or recursive glob patterns")
    parser.add_argument("--stdin", action="store_true", help="check standard input")
    parser.add_argument("--terms", type=Path, default=DEFAULT_TERMS)
    parser.add_argument("--symbols", type=Path, default=DEFAULT_SYMBOLS)
    parser.add_argument("--compounds", type=Path, default=DEFAULT_COMPOUNDS)
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
        compounds = load_terms(args.compounds)
        if not args.skip_symbols and not symbols:
            print(f"symbol list is empty: {args.symbols}", file=sys.stderr)
            return 2

        if args.stdin:
            count = check_text(sys.stdin.read(), "<stdin>", terms, symbols, compounds)
        else:
            count = 0
            paths = []
            for pattern in args.files:
                found = sorted(glob.glob(pattern, recursive=True))
                if not found:
                    raise OSError(f"no files match: {pattern}")
                paths.extend(Path(path) for path in found)
            for path in dict.fromkeys(paths):
                count += check_text(
                    path.read_text(encoding="utf-8"), str(path), terms, symbols, compounds
                )
    except (OSError, UnicodeError) as error:
        print(error, file=sys.stderr)
        return 2

    return 1 if count else 0


if __name__ == "__main__":
    raise SystemExit(main())
