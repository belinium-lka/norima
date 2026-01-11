#!/usr/bin/env python3
"""Tiny Norima interpreter prototype.

This interpreter supports a minimal subset used by examples/hello.norm:
- variable assignment of string literals: `let name = "value";`
- `print(...)` where argument may be a string literal or identifier

It's intentionally tiny and forgiving — meant for fast iteration.
"""
import sys
from pathlib import Path

# Ensure repository root is on sys.path so `vm` can be imported when running
# this file directly (e.g. `python3 vm/interpreter.py`).
repo_root = Path(__file__).resolve().parents[1]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from vm import parser, runtime


def run_file(path: str) -> int:
    text = open(path, "r", encoding="utf-8").read()
    prog = parser.parse_src(text)
    env = runtime.Env()
    try:
        runtime.eval_program(prog, env)
    except Exception as e:
        print(f"Runtime error: {e}")
        return 1
    return 0


def main(argv):
    if len(argv) < 2:
        print("Usage: interpreter.py <file.norm>")
        return 2
    return run_file(argv[1])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
