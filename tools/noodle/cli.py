#!/usr/bin/env python3
"""
Noodle CLI stub (noodle)

Initial commands: make, slurp, list, search, init, publish
"""
import argparse
import sys
from pathlib import Path
import subprocess


PKG_DIR = Path(__file__).resolve().parents[1] / "noodle" / "packages"


def cmd_install(name: str) -> int:
    pkg_path = PKG_DIR / name
    if not pkg_path.exists():
        print(f"error: package not found: {name}")
        return 2
    install_sh = pkg_path / "install.sh"
    if not install_sh.exists():
        print(f"error: package {name} has no install.sh")
        return 2
    print(f"Installing {name} from {pkg_path}")
    res = subprocess.run(["/bin/bash", str(install_sh)], check=False)
    return res.returncode


def main(argv=None):
    argv = argv or sys.argv[1:]
    p = argparse.ArgumentParser(prog='noodle')
    sub = p.add_subparsers(dest='command')
    sub.add_parser('install', help='Install a package').add_argument('name')
    sub.add_parser('help', help='Show help')
    args = p.parse_args(argv)
    if not args.command or args.command == 'help':
        p.print_help()
        return 0
    if args.command == 'install':
        return cmd_install(args.name)
    print(f"Unknown command: {args.command}")
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
