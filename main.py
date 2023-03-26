import sys

from stdlib import eval, from_list, symbols, resolve_maybe

sys.setrecursionlimit(200)


whitespace = set(" \n")


def skip_whitespace(i, inp):
    while i < len(inp) and inp[i] in whitespace:
        i += 1
    return (i, None)


def read_number(i, inp):  # reads number from i
    n = ""
    chars = set(" \n)")
    n += inp[i]
    i += 1
    while i < len(inp) and inp[i] not in chars:
        n += inp[i]
        i += 1
    return (i, int(n))


def read_symbol(i, inp):
    chars = set(" \n)")
    symbol = ""
    while i < len(inp) and inp[i] not in chars:
        symbol += inp[i]
        i += 1
    return (i, symbol)


def read_hashtag(i, inp):
    chars = set(" \n)")
    symbol = ""
    while i < len(inp) and inp[i] not in chars:
        symbol += inp[i]
        i += 1
    return (i, symbol == "#t")


numbers = set("1234567890")


def parse(i, inp):
    (i, _) = skip_whitespace(i, inp)
    if i >= len(inp):
        return (i, "oh shit")
    val_only = inp[i] != "("
    if not val_only:
        i += 1
    s_expr = []
    while i < len(inp) and inp[i] != ")":
        (i, _) = skip_whitespace(i, inp)
        if inp[i] in numbers:
            (i, val) = read_number(i, inp)
        elif inp[i] == "#":
            (i, val) = read_hashtag(i, inp)
        elif inp[i] == "'":
            (i, val) = parse(i + 1, inp)
            # print("val!", val)
            val = from_list(["quote", val])
            # print("val2!", val)
        elif inp[i] == "(":
            (i, val) = parse(i, inp)
        elif inp[i] not in whitespace:
            (i, val) = read_symbol(i, inp)
        else:
            val = "???????????"
        s_expr.append(val)

    i += 1
    if s_expr == []:
        return (i, "oh shit")
    if val_only:
        s_expr = s_expr[0]
    else:
        s_expr = from_list(s_expr)
    return (i, s_expr)


def top_eval(i, inp, symbols):
    (i, s_expr) = parse(i, inp)
    if s_expr == "oh shit":
        return (i, "oh shit")
    return (i, resolve_maybe(eval(s_expr, symbols)))


inp = open("messing.scm").read()
ti = 0
while ti < len(inp):
    (ti, result) = top_eval(ti, inp, symbols)
    if result == "oh shit":
        break
