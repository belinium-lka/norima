#!/usr/bin/env python3
"""Module entrypoint for the `hem` CLI.

This mirrors the behavior of the `tools/hem/hem` script but exposes a
`main()` function suitable for packaging entry points.
"""
from __future__ import annotations

import sys
from pathlib import Path
import textwrap
import importlib.util
import os


COMMAND_STUBS = [
    "init",
    "new",
    "build",
    "test",
    "fmt",
    "lint",
    "pkg",
    "install",
    "uninstall",
    "update",
    "version",
    "repl",
    "serve",
    "start",
    "stop",
    "status",
    "config",
    "login",
    "logout",
    "publish",
    "unpublish",
    "search",
    "deps",
    "lock",
    "unlock",
    "migrate",
    "seed",
    "docs",
    "clean",
    "cache",
    "release",
    "tag",
    "bump",
    "commit",
    "changelog",
    "smoke",
    "bench",
    "profile",
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def import_interpreter():
    try:
        from vm import interpreter

        return interpreter
    except Exception:
        pass

    interp_path = repo_root() / "vm" / "interpreter.py"
    if not interp_path.exists():
        raise RuntimeError(f"interpreter not found at {interp_path}")

    spec = importlib.util.spec_from_file_location("norima_vm_interpreter", str(interp_path))
    mod = importlib.util.module_from_spec(spec)
    loader = spec.loader
    assert loader is not None
    loader.exec_module(mod)
    return mod


def cmd_run(path: str) -> int:
    interp = import_interpreter()
    fp = Path(path)
    if not fp.exists():
        print(f"error: file not found: {path}")
        return 2
    return interp.run_file(str(fp))


def cmd_create_dev_go() -> int:
    root = repo_root()
    dev_dir = root / "dev"
    dev_dir.mkdir(exist_ok=True)

    server_py = dev_dir / "server.py"
    if server_py.exists():
        print(f"dev server already exists: {server_py}")
        return 0

    server_py.write_text(textwrap.dedent('''
        #!/usr/bin/env python3
        """Simple dev server scaffold created by `hem -c.dev go`.

        Run: python3 dev/server.py
        """
        import http.server
        import socketserver

        PORT = 8000

        class Handler(http.server.SimpleHTTPRequestHandler):
            pass

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"Dev server running at http://localhost:{PORT}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("Stopping dev server")
    '''))
    os.chmod(server_py, 0o755)

    readme = dev_dir / "README.md"
    readme.write_text("Created by `hem -c.dev go`. Run `python3 dev/server.py` to start.")

    print(f"Created dev server scaffold: {server_py}")
    return 0


def print_help() -> None:
    root = repo_root()
    msg = f"""
    hem — Norima runtime CLI (prototype)

    Usage:
      hem -run <file>        Run a .norm file
      hem -c.dev go          Create a dev server scaffold (dev/server.py)
      hem <command>          Run one of the many hem commands (stubbed)
      hem help               Show this help

    Note: This is a prototype. Install with the provided install script or
    `pip install .` to enable the `hem` console script.
    Repository root: {root}
    """
    print(textwrap.dedent(msg))


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    if not argv or argv[0] in ("help", "-h", "--help"):
        print_help()
        return 0

    cmd = argv[0].lstrip("-")

    # Special flags
    if cmd == "run":
        if len(argv) < 2:
            print("error: `-run` requires a file argument")
            return 2
        return cmd_run(argv[1])

    if cmd == "c.dev":
        if len(argv) < 2:
            print("error: `-c.dev` requires a subcommand (e.g. go)")
            return 2
        sub = argv[1]
        if sub == "go":
            return cmd_create_dev_go()
        print(f"Unknown `-c.dev` subcommand: {sub}")
        return 2

    # Generic stubs for many hem commands
    if cmd in COMMAND_STUBS:
        print(f"hem: stub: '{cmd}' — not implemented yet")
        return 0

    print(f"Unknown command: {cmd}")
    print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
