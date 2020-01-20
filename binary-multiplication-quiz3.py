#!/usr/bin/env python3

# This implements n-bit binary multiplication

from z3 import *

bits = 10

s = Solver()

# debug help
def print_add(*args):
    _add = s.add
    print(args)
    _add(*args)
    s.add = print_add


vars = 0
_bool = Bool
def counting_bool(*args):
    global vars
    vars += 1
    return _bool(*args)
Bool = counting_bool

# numbers to add, and result
# the indexing on bit here is weird, but mirrors the course
a = [Bool('a%d' % (i + 1)) for i in range(bits)]  # addend
b = [Bool('b%d' % (i + 1)) for i in range(bits)]  # addend
d = [Bool('d%d' % (i + 1)) for i in range(bits)]  # result

# intermediate values for steps of multiplication
r = [[Bool('r%d%d' % (i, j)) for j in range(bits)]
     for i in range(bits - 1)]
r.append(None)  # filled in by mul operation

rr = [[Bool('s%d%d' % (i, j)) for j in range(bits)]
      for i in range(bits - 1)]



def add(a, b, d, i):
    """Add a and b together to produce d."""
    assert(len(a) == len(b) == len(d))
    bits = len(a)  # bits per number

    # set up carry vector
    c = [Bool('c%s%d' % (i, j)) for j in range(bits + 1)]    # carries

    result = [
        Not(c[0]),  # no carry out (overflow is unsat)
        Not(c[-1])  # no carry in
    ]

    # result is true iff 1 or 3 of ai, bi, ci are true
    for i in range(bits):
        result += [d[i] == (a[i] == (b[i] == c[i+1]))]

    # carries
    for i in range(bits):
        result += [
            c[i] == Or(
                And(a[i], b[i]),
                And(a[i], c[i+1]),
                And(b[i], c[i+1])
            )
        ]

    return And(*result)


def dup(x, y):
    """y = 2x: multiply a binary number by two"""
    assert len(x) == len(y)
    bits = len(x)

    result = [
        Not(x[0]),   # overflow is unsat
        Not(y[-1])   # y must be even
    ]

    # y is x shifted left by one position
    for i in range(bits - 1):
        result += [y[i] == x[i+1]]

    return And(*result)


def mul(a, b, d):
    """r = a * b"""
    assert len(a) == len(b) == len(d)
    bits = len(a)

    # make r equal to the intermediate r values defined above, with d as
    # its last row.  This forces the result to go into d.
    r[-1] = d

    result = []

    # result starts at zero
    result += [Not(r[0][j]) for j in range(bits)]

    # iterative shift/add
    for i in range(bits - 1):
        result += [
            dup(r[i], rr[i]),  # rr = 2r
            Implies(b[i+1],      add(a, rr[i], r[i+1], i)),
            Implies(Not(b[i+1]), And(*[
                rr[i][j] == r[i+1][j] for j in range(bits)
            ]))
        ]

    return And(*result)


def number(num, values):
    assert len(values) == bits
    return [n if val else Not(n)
            for n, val in zip(num, values)]



s.add(mul(a, b, d))
s.add(*number(a, [0, 0, 0, 0, 0, 1, 0, 1, 0, 1]))
s.add(*number(b, [0, 0, 0, 0, 0, 0, 1, 0, 1, 1]))

result = s.check()
print(result)

def print_binary(n, prepend=""):
    """Print a binary number from an array"""
    print(prepend, end="")
    for j in range(bits):
        print(ib(m[n[j]]), end="")

if result == sat:
    m = s.model()
    ib = lambda x: int(bool(x))
    print()

    print_binary(a, "a = ")
    print()

    print_binary(b, "b = ")
    print()
    print()

    # print all the intermediate values so we can
    # see what happens
    for i in range(bits - 1):    # steps
        print("r%dj:  " % i, end="")
        print_binary(r[i])

        print("  s%dj:  " % i, end="")
        print_binary(rr[i])
        print()

    print()

    print_binary(d, "d = ")
    print()
else:
    print("core:", s.unsat_core())

print(vars, "variables")
