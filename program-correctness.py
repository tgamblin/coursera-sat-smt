#!/usr/bin/env python3

"""Program Correctness

Consider the following program:

    a := 1;
    b := 1;

    for i := 1 to 10 do
        if ? then {
            a := a + 2b;
            b := b + i;
        } else {
            b := a + b;
            a := a + i;
        };

    if b = 600 + n then crash

Here '?' is an unknown test that may yield false or true in any
situation.

Establish for which values of n = 1,2...,10 it is safe, that is, will not
reach 'crash'.

Concatenate your answers to one number, so if only 3,5,8 would be safe,
enter number 358.

Answer: 5679

"""
import sys

from z3 import *

steps = 10
solver = Solver()

# a0..a10 and b0..b10
a = [Int('a_%d' % i) for i in range(steps + 1)]
b = [Int('b_%d' % i) for i in range(steps + 1)]

# value of the question mark at each step
q = [None] + [Bool('q_%d' % i) for i in range(1, steps + 1)]


solver.add(a[0] == 1)
solver.add(b[0] == 1)

for i in range(1, steps + 1):
    solver.add(
        Or(
            And(q[i],
                a[i] == a[i - 1] + 2 * b[i - 1],
                b[i] == b[i - 1] + i),
            And(Not(q[i]),
                b[i] == a[i - 1] + b[i - 1],
                a[i] == a[i - 1] + i)
        )
    )


solver.add(b[10] == 600 + int(sys.argv[1]))
result = solver.check()
print(result)
if result == sat:
    model = solver.model()
    print(model)
