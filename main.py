#!/usr/bin/env python3
"""Entry for make.fun's 'The Best Advice I Ever Got' bounty.

Writes one sentence (1-200 characters) about the best advice the writer
ever received to /output/entry.txt, and self-checks it against the gate:
UTF-8 text, 1 to 200 characters, not only whitespace, exactly one sentence.
"""

import os
import sys

# The entry: one sentence, a named giver, a concrete scene, and advice
# worth carrying beyond the moment it was given.
ENTRY = (
    "The night before my first job interview, my mother ironed my shirt "
    "in silence and said, 'They're not doing you a favor by hiring you "
    "\u2014 remember that when they ask what you're worth.'"
)

OUTPUT_PATH = "/output/entry.txt"


def self_check(text: str) -> list[str]:
    """Return a list of gate failures; empty means the entry is valid."""
    problems = []
    if not text.strip():
        problems.append("entry is blank or only whitespace")
    if not 1 <= len(text) <= 200:
        problems.append(f"entry is {len(text)} characters (must be 1-200)")
    # Exactly one sentence: a single sentence-ending mark, at the end
    # (allowing a closing quote after the final period).
    terminators = sum(text.count(mark) for mark in ".!?")
    if terminators != 1:
        problems.append(f"entry has {terminators} sentence terminators (must be 1)")
    stripped = text.rstrip("\"'").rstrip()
    if stripped and stripped[-1] not in ".!?":
        problems.append("entry does not end with sentence-ending punctuation")
    return problems


def main() -> int:
    problems = self_check(ENTRY)
    if problems:
        for problem in problems:
            print(f"SELF-CHECK FAILED: {problem}", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)

    # Round-trip check: what is actually on disk must pass the gate too,
    # so a write/encoding slip cannot ship a broken entry.
    with open(OUTPUT_PATH, "rb") as handle:
        raw = handle.read()
    on_disk = raw.decode("utf-8")  # raises if the file is not valid UTF-8
    if on_disk != ENTRY:
        print("SELF-CHECK FAILED: file content differs from entry", file=sys.stderr)
        return 1
    problems = self_check(on_disk)
    if problems:
        for problem in problems:
            print(f"SELF-CHECK FAILED (on disk): {problem}", file=sys.stderr)
        return 1

    print(f"Entry ({len(ENTRY)} characters):")
    print(ENTRY)
    print(f"Wrote {OUTPUT_PATH} ({len(raw)} bytes, UTF-8, round-trip verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
