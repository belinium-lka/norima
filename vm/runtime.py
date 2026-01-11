"""Runtime evaluator for Norima AST (MVP).

Executes the AST produced by `vm.parser`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from vm import parser


class ReturnException(Exception):
    def __init__(self, value: Any):
        self.value = value


class Env:
    def __init__(self, parent: Optional["Env"] = None):
        self.vars: Dict[str, Any] = {}
        self.funcs: Dict[str, parser.FnDef] = {}
        self.parent = parent

    def get(self, name: str) -> Any:
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(name)

    def set(self, name: str, val: Any) -> None:
        self.vars[name] = val

    def define_fn(self, name: str, fn: parser.FnDef) -> None:
        self.funcs[name] = fn

    def get_fn(self, name: str) -> parser.FnDef:
        if name in self.funcs:
            return self.funcs[name]
        if self.parent:
            return self.parent.get_fn(name)
        raise NameError(f"function {name} not found")


def eval_program(prog: parser.Program, env: Env) -> None:
    for stmt in prog.body:
        eval_stmt(stmt, env)


def eval_stmt(node: parser.Node, env: Env) -> Any:
    if isinstance(node, parser.Let):
        val = eval_expr(node.expr, env)
        env.set(node.name, val)
        return None
    if isinstance(node, parser.FnDef):
        env.define_fn(node.name, node)
        return None
    if isinstance(node, parser.Return):
        val = eval_expr(node.expr, env)
        raise ReturnException(val)
    if isinstance(node, parser.ExprStmt):
        return eval_expr(node.expr, env)
    raise RuntimeError(f"Unknown statement: {node}")


def eval_expr(node: parser.Node, env: Env) -> Any:
    if isinstance(node, parser.Number):
        return node.value
    if isinstance(node, parser.Str):
        return node.value
    if isinstance(node, parser.Ident):
        return env.get(node.name)
    if isinstance(node, parser.Binary):
        l = eval_expr(node.left, env)
        r = eval_expr(node.right, env)
        if node.op == "+":
            return l + r
        if node.op == "-":
            return l - r
        if node.op == "*":
            return l * r
        if node.op == "/":
            return l / r
        if node.op == "=":
            # assignment as expression not supported at top level
            raise RuntimeError("Assignment operator not supported in expressions")
        raise RuntimeError(f"Unknown binary op {node.op}")
    if isinstance(node, parser.Call):
        # builtin: print
        if node.callee == "print":
            args = [eval_expr(a, env) for a in node.args]
            print(*args)
            return None
        # user function
        fn = env.get_fn(node.callee)
        # prepare function env
        fn_env = Env(parent=env)
        # bind params
        for name, arg_node in zip(fn.params, node.args):
            fn_env.set(name, eval_expr(arg_node, env))
        try:
            for s in fn.body:
                eval_stmt(s, fn_env)
        except ReturnException as r:
            return r.value
        return None
    raise RuntimeError(f"Unknown expr: {node}")
