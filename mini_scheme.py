from typing import Tuple

TERMINATORS = set(" \t\n)")
Sexpr = int | str | list

def parse_number(s: str, i: int) -> Tuple[int, int]:
    acc = ""
    while i < len(s) and s[i].isdigit():
        acc += s[i]
        i += 1
    return int(acc), i

def parse_symbol(s: str, i: int) -> Tuple[str, int]:
    acc = ""
    while i < len(s) and s[i] not in TERMINATORS:
        acc += s[i]
        i += 1
    return acc, i

def until_whitespace(s: str, i: int) -> int:
    while i < len(s) and s[i] in " \n\t":
        i += 1
    return i

def parse_list(s: str, i: int) -> Tuple[list, int]:
    acc = []
    i += 1
    while i < len(s) and s[i] != ")":
        val, i = parse_sexpr(s, i)
        acc.append(val)
        until_whitespace(s, i)
    return acc, i+1

def parse_sexpr(s: str, i: int) -> Tuple[Sexpr, int]:
    i = until_whitespace(s, i)
    if s[i].isdigit():
        return parse_number(s, i)
    if s[i] == "(":
        return parse_list(s, i)
    return parse_symbol(s, i)

def eval(sexpr: Sexpr) -> int:
    if isinstance(sexpr, int):
        return sexpr
    op, first, second = sexpr
    first_evaled = eval(first)
    second_evaled = eval(second)
    if op == "+":
        return first_evaled + second_evaled
    if op == "-":
        return first_evaled - second_evaled
    if op == "*":
        return first_evaled * second_evaled
    if op == "/":
        return int(first_evaled / second_evaled)
    return 0

while True:
    expression = input("Please enter an expression: ")
    parsed_val, i = parse_sexpr(expression, 0)
    print(eval(parsed_val))
