#!/usr/bin/env python3
"""Everyday Wonder, Two Days to Find the Line — make.fun entry.

Writes one sentence (at most 200 characters) that makes a small
everyday moment strange and new, to /output/entry.txt (or
$MAKEFUN_OUTPUT_DIR / $OUTPUT_DIR when set).
"""

import os
import re
import sys

ENTRY = (
    "At 3 a.m. the fridge hummed a note I had never noticed, "
    "and for a moment the kitchen sounded like it was keeping me company."
)


def validate_entry(text: str) -> None:
    """Gate: 1-200 chars, one sentence, no empty/whitespace-only text."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if len(text) > 200:
        raise ValueError(f"entry is {len(text)} chars, over the 200 cap")
    if text.strip() != text:
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    # Exactly one sentence: it must end in a single terminal period, and
    # contain no other sentence boundary. A period counts as a boundary
    # only when followed by a space and an uppercase letter, so
    # abbreviations such as "3 a.m." stay valid.
    if not text.endswith("."):
        raise ValueError("entry must end in '.'")
    body = text[:-1]
    if re.search(r"[.!?]\s+[A-Z]", body):
        raise ValueError("entry must be exactly one sentence")
    if "!" in body or "?" in body:
        raise ValueError("entry must not contain '!' or '?'")


def output_dir() -> str:
    return (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )


def main() -> int:
    validate_entry(ENTRY)
    out = output_dir()
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
