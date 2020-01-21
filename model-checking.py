#!/usr/bin/env python3

# Bounded model checking

#
# Start with one marble.
#
# We do steps in which either:
#   a. one marble is added, or
#   b. the number of marbles is doubled
#
# Find min steps to 1,000 marbles
#

from z3 import *


def marbles(k):
    s = Solver()

    # M is the number of marrbles at step i (int) -> int
    m = Function("m", IntSort(), IntSort())

    s.add(m(0) == 1)
    s.add(m(k-1) == 1000)

    for i in range(k):
        s.add(Or(
            m(i) == m(i - 1) + 1,
            m(i) == 2 * m(i - 1)
        ))

    result = s.check()

    if result == sat:
        print("Found minimal solution at %d:" % k)
        model = s.model()
        for i in range(k):
            print(i, model.evaluate(m(i)))
        return True

    return False


marbles(1000)

#for i in range(1, 20):
#    if marbles(i):
#        break
