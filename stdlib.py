class TailCall:
    def __init__(self, s_expr, scope):
        # flattens the tail call if it happens to point to one
        if isinstance(s_expr, TailCall):
            self = s_expr
        else:
            self.call = lambda: eval(s_expr, scope)

    def resolve(self):
        t = self
        while isinstance(t, TailCall):
            t = t.call()
        return t


class SchemeFunc:
    def __init__(self, fn):
        self.fn = fn

    def evaluate(self, args, scope):  # resolve tail calls after the fn
        return self.fn(eval_all(args, scope))


class SchemeMacro:
    def __init__(self, macro):
        self.macro = macro

    def evaluate(self, args, scope):
        return self.macro(args, scope)


class Cons:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __iter__(self):
        cns = self
        while isinstance(cns, Cons):
            yield cns.car
            cns = cns.cdr

    def __repr__(self):
        out = "("
        t = 0
        for i in self:
            t += 1
            out += i.__repr__() + " "
        print(t)
        return out[:-1] + ")"

    def __len__(self):
        return len(list(iter(self)))


class EmptyCons:
    def __init__(self):
        pass

    def __bool__(self):
        return False

    def __iter__(self):
        return iter([])


def car(args):
    cns = args.car
    return cns.car


def cdr(args):
    cns = args.car
    return cns.cdr


def cons(args):
    a, b = args
    return Cons(a, b)


def from_list(alist):
    t = EmptyCons()
    for v in reversed(alist):
        t = Cons(v, t)
    return t


def resolve_maybe(maybe):
    return maybe.resolve() if isinstance(maybe, TailCall) else maybe


def eval_all(args, syms):
    maybe_unresolved = map(lambda arg: eval(arg, syms), args)
    result = list(map(resolve_maybe, maybe_unresolved))
    return from_list(result)


def eval(s_expr, syms):
    if isinstance(s_expr, str):
        return syms[s_expr]
    if isinstance(s_expr, TailCall):
        s_expr = s_expr.resolve()
    if not isinstance(s_expr, Cons):
        return s_expr
    header = (
        eval(s_expr.car, syms) if isinstance(s_expr.car, Cons) else syms[s_expr.car]
    )
    args = s_expr.cdr
    t = header.evaluate(args, syms)
    return t


def add(vals):
    return sum(vals)


def mult(vals):
    q = 1
    for v in vals:
        q *= v
    return q


def sub(vals):
    if len(vals) < 1:
        raise Exception("needs at least 1 arg")
    q = vals.car
    for v in vals.cdr:
        q -= v
    return q


def div(vals):
    if len(vals) < 1:
        raise Exception("needs at least 1 arg")
    first = vals.car
    for v in vals.cdr:
        first /= v
    return first


def bind(scope, new_symbols, values):
    return {**scope, **dict(zip(new_symbols, values))}


def lmbd(args, scope, rec=None):
    new_symbols, s_expr = args
    fn = SchemeFunc(lambda args: TailCall(s_expr, bind(scope, new_symbols, args)))
    if rec:
        scope[rec] = fn
    return fn


def define(args, scope):
    new_symbols, s_expr = args
    # print({**symbols, **dict(zip(new_symbols, args))})
    fn = lmbd([new_symbols.cdr] + [s_expr], scope, new_symbols.car)
    symbols[new_symbols.car] = fn


def s_if(args, scope):
    bool_body, success_clause, fail_clause = args
    if eval(bool_body, scope):
        return TailCall(success_clause, scope)
    return TailCall(fail_clause, scope)


def lt(args):
    first, second = args
    return first < second


def gt(args):
    first, second = args
    return first > second


def eq(args):
    first, second = args
    return first == second


def display(args):
    return print(*args)


def s_or(args, scope):
    first, second = args
    if eval(first, scope):
        return True
    return eval(second, scope)


def s_and(args, scope):
    first, second = args
    if not eval(first, scope):
        return False
    return eval(second, scope)


def quote(args, scope):
    first = args.car
    return first


symbols = {
    "+": SchemeFunc(add),
    "-": SchemeFunc(sub),
    "*": SchemeFunc(mult),
    "/": SchemeFunc(div),
    "<": SchemeFunc(lt),
    ">": SchemeFunc(gt),
    "=": SchemeFunc(eq),
    "display": SchemeFunc(display),
    "define": SchemeMacro(define),
    "lambda": SchemeMacro(lmbd),
    "if": SchemeMacro(s_if),
    "or": SchemeMacro(s_or),
    "and": SchemeMacro(s_and),
    "quote": SchemeMacro(quote),
    "car": SchemeFunc(car),
    "cdr": SchemeFunc(cdr),
    "cons": SchemeFunc(cons),
}
