from typing import Iterable
from enum import IntEnum, auto

class OpType(IntEnum):
    add = auto()
    sub = auto()
    mul = auto()
    div = auto()
    parenl = auto()
    parenr = auto()
    comma = auto()

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
parenl = Op(OpType.parenl, -1, "")
parenr = Op(OpType.parenr, -1, "")
comma = Op(OpType.comma, -1, ",")

def is_empty(l: list | tuple | Iterable):
    return len(l) == 0

def is_precedent_op(a: Op, b: Op):
    """Checks if a is more precedent than b"""
    return a.precedence >= b.precedence

def get_precedent_op(a: Op, b: Op):
    """Checks and returns the more precedent operator if equal sends first operator"""
    return a if a.precedence > b.precedence else b

def infix_to_postfix(expr: str) -> str:
    stk = []
    current = 0
    def last_is_paren() -> bool:
        return stk[-1] in (parenl, parenr) if not is_empty(stk) else False
    def peek() -> str:
        return expr[current+1] if current + 1 < len(expr) else ""
    ret = " "
    while current < len(expr):
        i = expr[current]
        if i.isspace():
            if ret[-1] != " ": ret += " "
        elif i == "+":
            while not is_empty(stk) and is_precedent_op(stk[-1], add) and not last_is_paren(): 
                ret += f"{stk.pop()} "
            stk.append(add)
        elif i == "-":
            while not is_empty(stk) and is_precedent_op(stk[-1], sub) and not last_is_paren(): 
                ret += f"{stk.pop()} "
            stk.append(sub)
        elif i == "*":
            while not is_empty(stk) and is_precedent_op(stk[-1], mul) and not last_is_paren(): 
                ret += f"{stk.pop()} "
            stk.append(mul)
        elif i == "/":
            while not is_empty(stk) and is_precedent_op(stk[-1], div) and not last_is_paren(): 
                ret += f"{stk.pop()} "
            stk.append(div)
        elif i == "%":
            while not is_empty(stk) and is_precedent_op(stk[-1], mod) and not last_is_paren(): 
                ret += f"{stk.pop()} "
            stk.append(mod)
        elif i == ")":
            while not is_empty(stk) and not last_is_paren(): 
                ret += f"{stk.pop()} "
            stk.pop()
        elif i == "(":
            stk.append(parenl)
        elif i == ',':
            while not is_empty(stk) and not last_is_paren():
                ret += f"{stk.pop()} "
        elif i.isnumeric():
            dot_used = False
            ret += i
            while peek().isnumeric() or (peek() == '.' and not dot_used):
                if peek() == '.': dot_used = True
                ret += peek()
                current += 1
            ret += " "
        else:
            ret += i
            if peek() in (' ', '+', '-', '*', '/', '(', ')'):
                ret += ' '
        current += 1
    while not is_empty(stk):
        ret += f"{stk.pop()} "
    return ret[1:]

def main():
    print('Press <Ctrl> + D or <Ctrl> + C to exit')
    while True:
        try:
            get = input('Enter infix: ')
            print(f'Postfix form: {infix_to_postfix(get)}')
        except EOFError: break
        except KeyboardInterrupt: break

if __name__ == '__main__':
    main()
