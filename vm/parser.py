"""Simple recursive-descent parser for Norima (MVP subset).

Produces a basic AST consumed by `vm.runtime`.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Any


Token = tuple[str, str]


def tokenize(src: str) -> List[Token]:
    token_spec = [
        ("NUMBER", r"\d+(?:\.\d+)?"),
        ("STRING", r'"(.*?)"'),
        ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("OP", r"\+|\-|\*|/|=|,"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("LBRACE", r"\{"),
        ("RBRACE", r"\}"),
        ("SEM", r";"),
        ("SKIP", r"[ \t\r\n]+"),
        ("MISMATCH", r".")
    ]

    tok_regex = "|".join(f"(?P<{n}>{p})" for n, p in token_spec)
    tokens: List[Token] = []
    for m in re.finditer(tok_regex, src):
        kind = m.lastgroup
        value = m.group(0)
        if kind == "SKIP":
            continue
        if kind == "STRING":
            # strip surrounding quotes
            value = value[1:-1]
        tokens.append((kind, value))
    return tokens


@dataclass
class Node:
    pass


@dataclass
class Program(Node):
    body: List[Node]


@dataclass
class Let(Node):
    name: str
    expr: Node


@dataclass
class FnDef(Node):
    name: str
    params: List[str]
    body: List[Node]


@dataclass
class Return(Node):
    expr: Optional[Node]


@dataclass
class ExprStmt(Node):
    expr: Node


@dataclass
class Call(Node):
    callee: str
    args: List[Node]


@dataclass
class Binary(Node):
    op: str
    left: Node
    right: Node


@dataclass
class Number(Node):
    value: float


@dataclass
class Str(Node):
    value: str


@dataclass
class Ident(Node):
    name: str


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Optional[Token]:
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]

    def eat(self, kind: str | None = None) -> Token:
        t = self.peek()
        if t is None:
            raise SyntaxError("Unexpected EOF")
        if kind and t[0] != kind:
            raise SyntaxError(f"Expected {kind}, got {t}")
        self.pos += 1
        return t

    def parse(self) -> Program:
        stmts: List[Node] = []
        while self.peek() is not None:
            stmts.append(self.parse_statement())
        return Program(stmts)

    def parse_statement(self) -> Node:
        t = self.peek()
        if t[0] == "IDENT" and t[1] == "let":
            self.eat("IDENT")
            name = self.eat("IDENT")[1]
            self.eat("OP")  # =
            expr = self.parse_expression()
            self.eat("SEM")
            return Let(name, expr)

        if t[0] == "IDENT" and t[1] == "fn":
            self.eat("IDENT")
            name = self.eat("IDENT")[1]
            self.eat("LPAREN")
            params: List[str] = []
            if self.peek() and self.peek()[0] == "IDENT":
                params.append(self.eat("IDENT")[1])
                while self.peek() and self.peek()[0] == "OP" and self.peek()[1] == ",":
                    self.eat("OP")
                    params.append(self.eat("IDENT")[1])
            self.eat("RPAREN")
            self.eat("LBRACE")
            body: List[Node] = []
            while self.peek() and self.peek()[0] != "RBRACE":
                if self.peek()[0] == "IDENT" and self.peek()[1] == "return":
                    self.eat("IDENT")
                    expr = self.parse_expression()
                    self.eat("SEM")
                    body.append(Return(expr))
                else:
                    body.append(self.parse_statement())
            self.eat("RBRACE")
            return FnDef(name, params, body)

        if t[0] == "IDENT" and t[1] == "return":
            self.eat("IDENT")
            expr = self.parse_expression()
            self.eat("SEM")
            return Return(expr)

        # expression statement (e.g., call)
        expr = self.parse_expression()
        self.eat("SEM")
        return ExprStmt(expr)

    # Expression parsing (precedence climbing)
    def parse_expression(self, min_prec=0) -> Node:
        node = self.parse_primary()
        while True:
            t = self.peek()
            if t is None or t[0] not in ("OP",):
                break
            op = t[1]
            prec = self._prec(op)
            if prec < min_prec:
                break
            self.eat("OP")
            rhs = self.parse_expression(prec + 1)
            node = Binary(op, node, rhs)
        return node

    def _prec(self, op: str) -> int:
        if op in ("+", "-"):
            return 10
        if op in ("*", "/"):
            return 20
        if op == "=":
            return 1
        return 0

    def parse_primary(self) -> Node:
        t = self.peek()
        if t is None:
            raise SyntaxError("Unexpected EOF in expression")
        if t[0] == "NUMBER":
            self.eat("NUMBER")
            return Number(float(t[1]))
        if t[0] == "STRING":
            self.eat("STRING")
            return Str(t[1])
        if t[0] == "IDENT":
            name = self.eat("IDENT")[1]
            # call?
            if self.peek() and self.peek()[0] == "LPAREN":
                self.eat("LPAREN")
                args: List[Node] = []
                if self.peek() and self.peek()[0] != "RPAREN":
                    args.append(self.parse_expression())
                    while self.peek() and self.peek()[0] == "OP" and self.peek()[1] == ",":
                        self.eat("OP")
                        args.append(self.parse_expression())
                self.eat("RPAREN")
                return Call(name, args)
            return Ident(name)
        if t[0] == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_expression()
            self.eat("RPAREN")
            return node
        raise SyntaxError(f"Unexpected token {t}")


def parse_src(src: str) -> Program:
    toks = tokenize(src)
    p = Parser(toks)
    return p.parse()
