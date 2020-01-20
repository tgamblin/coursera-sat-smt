#!/usr/bin/env python3

# This implements n-bit binary multiplication

from z3 import *

bits = 10

s = Solver()

# f represents positions on the board [int, int] -> int
# and maps them to their values
f = Function("f", IntSort(), IntSort(), IntSort())

# every cell value is in 1..9
for i in range(1, 10):
    for j in range(1, 10):
        s.add(And(f(i, j) >= 1, f(i, j) <= 9))

# every row distinct
for i in range(1, 10):
    row = [f(i, j) for j in range(1, 10)]
    s.add(Distinct(*row))

# every col distinct
for j in range(1, 10):
    col = [f(i, j) for i in range(1, 10)]
    s.add(Distinct(*col))

# every square distinct
for q in range(3):
    for r in range(3):
        square = []
        for i in range(1, 4):
            for j in range(1, 4):
                square.append(
                    f(3 * q + i, 3 * r + j))
        s.add(Distinct(*square))


# initial puzzle
init = [
    [0, 0, 9,  8, 5, 6,  0, 0, 0],
    [0, 8, 0,  0, 0, 9,  0, 0, 0],
    [2, 0, 0,  0, 0, 7,  0, 0, 0],

    [7, 0, 0,  0, 0, 1,  3, 9, 6],
    [9, 0, 0,  0, 6, 0,  0, 0, 5],
    [5, 3, 6,  2, 0, 0,  0, 0, 7],

    [0, 0, 0,  9, 0, 0,  0, 0, 1],
    [0, 0, 0,  3, 0, 0,  0, 6, 0],
    [0, 0, 0,  6, 8, 2,  4, 0, 0],
]

# set up puzzle
for i in range(9):
    for j in range(9):
        if init[i][j]:
            s.add(f(i + 1, j + 1) == init[i][j])

result = s.check()
print(result)

if result == sat:
    m = s.model()

    print()
    for i in range(1, 10):
        for j in range(1, 10):
            print(m.evaluate(f(i, j)), end=" ")
            if j % 3 == 0:
                print(" ", end="")
        if i % 3 == 0:
            print()
        print()
