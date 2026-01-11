#!/usr/bin/env python3
"""
Norima CLI stub (norima)

This is an initial prototype CLI to be expanded.
"""
import argparse
import sys
from pathlib import Path
from vm import interpreter


def cmd_run(path: str) -> int:
    p = Path(path)
    if not p.exists():
        print(f"error: file not found: {path}")
        return 2
    return interpreter.run_file(str(p))


def main(argv=None):
    argv = argv or sys.argv[1:]
    p = argparse.ArgumentParser(prog='norima')
    sub = p.add_subparsers(dest='command')
    sub.add_parser('run', help='Run a .norm program').add_argument('file')
    sub.add_parser('new', help='Create a new Norima project').add_argument('name')
    sub.add_parser('help', help='Show help')
    args = p.parse_args(argv)
    if not args.command or args.command == 'help':
        p.print_help()
        return 0
    if args.command == 'run':
        return cmd_run(args.file)
    if args.command == 'new':
        # scaffold a simple project
        name = args.name
        from pathlib import Path
        p = Path(name)
        if p.exists():
            print(f"error: path exists: {p}")
            return 2
        p.mkdir(parents=True)
        (p / 'main.norm').write_text('fn main() {\n  print("Hello from '+name+'!");\n}\n')
        (p / 'norima.toml').write_text('[project]\nname = "'+name+'"\n')
        print(f"Created new Norima project: {p}")
        return 0
    print(f"Unknown command: {args.command}")
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
