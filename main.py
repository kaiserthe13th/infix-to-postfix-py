from typing import Iterable, List
from enum import IntEnum, auto

class OpType(IntEnum):
    add = auto()
    sub = auto()
    mul = auto()
    div = auto()
    parenl = auto()
    parenr = auto()
    comma = auto()
    Number = auto()
    Ident = auto()
    Reserved = auto()

class Op:
    def __init__(self, optyp: OpType, precedence: int, form: str):
        self.optyp = optyp
        self.precedence = precedence
        self.form = form

    def __str__(self): return self.form
    def __repr__(self): return self.form

add = Op(OpType.add, 0, "+")
sub = Op(OpType.sub, 0, "-")
mul = Op(OpType.mul, 1, "*")
div = Op(OpType.div, 1, "/")
mod = Op(OpType.div, 1, "%")
parenl = Op(OpType.parenl, -1, "(")
parenr = Op(OpType.parenr, -1, ")")
comma = Op(OpType.comma, -1, ",")

def is_empty(l: list | tuple | Iterable):
    return len(l) == 0

def is_precedent_op(a: Op, b: Op):
    """Checks if a is more precedent than b"""
    return a.precedence > b.precedence

def get_precedent_op(a: Op, b: Op):
    """Checks and returns the more precedent operator if equal sends first operator"""
    return a if a.precedence > b.precedence else b

def splits(expr: str) -> List[str]:
    expr = expr + ' '
    current = 0
    ret = []
    while len(expr) > current:
        t = ""
        c = expr[current]
        dot_used = False
        if c.isnumeric():
            while c.isnumeric() or c == '.':
                if c == '.':
                    if dot_used: break
                    else: dot_used = True
                t += c
                current += 1
                c = expr[current]
            if dot_used: current += 1
        elif c in ('+', '-', '/', '(', ')', '%', '*', ','):
            ret.append(c)
            current += 1
        elif c == ' ':
            current += 1
        else:
            while (c not in ('+', '-', '/', '(', ')', '%', '*', ' ', ',')):
                t += c
                current += 1
                c = expr[current]
        if t: ret.append(t)
    return ret

def parses(expr: List[str]) -> List[Op]:
    ret = []
    for i in expr:
        if i.isnumeric() or '.' in i:
            ret.append(Op(OpType.Number, 0, i))
        elif i == '+': ret.append(add)
        elif i == '-': ret.append(sub)
        elif i == '*': ret.append(mul)
        elif i == '/': ret.append(div)
        elif i == '%': ret.append(mod)
        elif i == '(': ret.append(parenl)
        elif i == ')': ret.append(parenr)
        elif i == ',': ret.append(comma)
        elif i in ('de', 'at', 'ver', 'işlev', 'iken', ':.', 'ise', 'yoksa', 'son', '->'): ret.append(Op(OpType.Reserved, 0, i))
        else: ret.append(Op(OpType.Ident, 0, i))
    return ret

def infix_to_postfix(expr: str) -> str:
    stk = []
    ret = ""
    sp = splits(expr)
    ps = parses(sp)
    current = 0
    while len(ps) > current:
        i = ps[current]
        if i.optyp == OpType.Reserved:
            while not is_empty(stk):
                ret += stk.pop().form + ' '
            ret += i.form + ' '
            current += 1
        elif i.optyp == OpType.Number or i.optyp == OpType.Ident:
            ret += i.form + ' '
            current += 1
        elif i == add:
            while not is_empty(stk) and not is_precedent_op(add, stk[-1]):
                ret += stk.pop().form + ' '
            stk.append(i)
            current += 1
        elif i == sub:
            while not is_empty(stk) and not is_precedent_op(sub, stk[-1]):
                ret += stk.pop().form + ' '
            stk.append(i)
            current += 1
        elif i == mul:
            while not is_empty(stk) and not is_precedent_op(mul, stk[-1]):
                ret += stk.pop().form + ' '
            stk.append(i)
            current += 1
        elif i == div:
            while not is_empty(stk) and not is_precedent_op(div, stk[-1]):
                ret += stk.pop().form + ' '
            stk.append(i)
            current += 1
        elif i == mod:
            while not is_empty(stk) and not is_precedent_op(mod, stk[-1]):
                ret += stk.pop().form + ' '
            stk.append(i)
            current += 1
        elif i == parenr:
            while not is_empty(stk) and stk[-1] != parenl:
                ret += stk.pop().form + ' '
            stk.pop()
            current += 1
        elif i == comma:
            while not is_empty(stk) and stk[-1] not in (parenl, comma):
                ret += stk.pop().form + ' '
            current += 1
        elif i == parenl:
            stk.append(i)
            current += 1
    while not is_empty(stk):
        ret += stk.pop().form + ' '
    return ret[:-1]

def main():
    print('Press <Ctrl> + D or <Ctrl> + C to exit')
    while True:
        try:
            get = input('Enter infix: ')
            print(f'Postfix form: {infix_to_postfix(get)}')
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            break

if __name__ == '__main__':
    main()
