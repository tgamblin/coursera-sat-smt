#!/usr/bin/env python3

# Sudoku variant where initial constraints are consecutive digits /
# restrictions that one cell be less than another instead of initial
# numbers.

from z3 import *

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


consecutive = [
    [(1, 2), (1, 3)], [(1, 4), (1, 5)], [(1, 7), (1, 8)],
    [(1, 6), (2, 6)],
    [(2, 7), (3, 7)],
    [(3, 2), (3, 3)], [(3, 4), (3, 5)], [(3, 5), (3, 6)],
    [(3, 7), (4, 7)], [(3, 9), (4, 9)],
    [(4, 3), (5, 3)], [(4, 7), (5, 7)], [(4, 9), (5, 9)],
    [(5, 1), (5, 2)], [(5, 2), (5, 3)], [(5, 4), (5, 5)],
    [(5, 6), (5, 7)], [(5, 8), (5, 9)],
    [(6, 3), (6, 4)],
    [(6, 3), (7, 3)], [(6, 4), (7, 4)], [(6, 6), (7, 6)], [(6, 7), (7, 7)],
    [(7, 3), (7, 4)],
    [(8, 6), (8, 7)],
]

# consecutive numbers
for pair in consecutive:
    c1, c2 = pair
    s.add(Or(
        f(*c2) - f(*c1) == 1,
        f(*c1) - f(*c2) == 1
    ))

# less than ranges
for i in range(5, 10):
    s.add(f(2, i - 1) < f(2, i))

for i in range(2, 7):
    s.add(f(4, i - 1) < f(4, i))

for i in range(7, 10):
    s.add(f(6, i - 1) < f(6, i))

for i in range(2, 7):
    s.add(f(8, i - 1) < f(8, i))


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
