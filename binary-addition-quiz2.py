#!/usr/bin/env python3

# This implements 4-bit binary addition in SAT.
# The addition looks like this:
#
#     c1 c2 c3 c4  # carries
#     a1 a2 a3 a4  # addend
#  +  b1 b2 b3 b4  # addend
# -------------------------
#     d1 d2 d3 d4  # result
#
# Bit 4 is the low bit, bit 1 is the high bit (to stay faithful to the
# way it was in the lecture)

from z3 import *
set_option(unsat_core=True)

bits = 4

s = Solver()

_add = s.add
def add(*args):
    print(args)
    _add(*args)

s.add = add

c0, c1, c2, c3, c4 = [Bool('c%d' % i) for i in range(bits + 1)]  # carries
a1, a2, a3, a4 = [Bool('a%d' % (i + 1)) for i in range(bits)]  # addend
b1, b2, b3, b4 = [Bool('b%d' % (i + 1)) for i in range(bits)]  # addend
d1, d2, d3, d4 = [Bool('d%d' % (i + 1)) for i in range(bits)]  # result

# result is true iff 1 or 3 of ai, bi, ci are true
s.add(d1 == (a1 == (b1 == c1)))
s.add(d2 == (a2 == (b2 == c2)))
s.add(d3 == (a3 == (b3 == c3)))
s.add(d4 == (a4 == (b4 == c4)))

# Carries
s.add(Not(c0))  # no carry out (overflow is unsat)
s.add(c0 == Or(And(a1, b1), And(a1, c1), And(b1, c1)))
s.add(c1 == Or(And(a2, b2), And(a2, c2), And(b2, c2)))
s.add(c2 == Or(And(a3, b3), And(a3, c3), And(b3, c3)))
s.add(c3 == Or(And(a4, b4), And(a4, c4), And(b4, c4)))
s.add(Not(c4))  # no carry in

#s.add(a1, a2,      Not(a3), a4)  # 13
#s.add(b1, Not(b2), b3,      b4)  # 11

s.add(Not(a1), a2,      Not(a3), a4)  # 5
s.add(Not(b1), Not(b2), b3,      b4)  # 3


#s.add(c4)

result = s.check()
print(result)

if result == sat:
    m = s.model()
    print(m)

    ib = lambda x: int(bool(x))
    print("d =", [ib(m[d1]), ib(m[d2]), ib(m[d3]), ib(m[d4])])
else:
    print("core:", s.unsat_core())
