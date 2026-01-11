# Norima Language — MVP Specification

This document describes a small, practical subset of the Norima language
designed for rapid prototyping and for building small projects.

Core concepts
- Files: `.norm` source files contain statements and function definitions.
- Statements end with a semicolon `;` except for block constructs.
- Expressions support numbers, strings, identifiers, function calls, and
  binary arithmetic operators `+ - * /` with usual precedence.

Syntax (examples)

- Variable declaration/assignment:

  let name = "value";

- Function definition:

  fn greet(name) {
    print("Hello, " + name);
  }

- Function call:

  greet("Norima");

- Return inside functions:

  fn add(a, b) {
    return a + b;
  }

Builtins
- `print(x)`: prints a value to stdout.

Semantics
- Variables are function-scoped. Functions are first-class within this MVP
  and stored in the module environment.
- The interpreter executes top-level statements in order.

Files and projects
- A Norima project is a directory containing a `main.norm` (entrypoint) and
  optionally more module files. The `norima new` command scaffolds a project.

Limitations
- No modules/imports in the MVP (imports may be added later).
- Error messages are simple and intended for development iteration.

This spec is intentionally small — it focuses on what is needed to build
and iterate on small Norima applications. Future work: module system,
type checker, standard library, optimizations, and an LSP server.
