#!/usr/bin/env python3

"""Job Scheduling

Ten jobs numbered from 1 to 10 have to be executed without interrupt, and
satisfying the following requirements:

- The running time of job i is i + 10, for i = 1, 2, . . . , 10.

- Job 3 may only start if jobs 1 and 2 have been finished.
- Job 6 may only start if jobs 2 and 4 have been finished.
- Job 7 may only start if jobs 1, 4 and 5 have been finished.
- Job 8 may only start if jobs 3 and 6 have been finished.
- Job 9 may only start if jobs 6 and 7 have been finished.
- Job 10 may only start if jobs 8 and 9 have been finished.

What is the minimal total running time?

(Hint: if you do not use minimize, you may do this by binary search)

Answer: 71

"""

from z3 import *

njobs = 10

# initial nones for one-based indexing
start   = [None] + [Int('start_%d' % i) for i in range(1, njobs + 1)]
end     = [None] + [Int('end_%d' % i) for i in range(1, njobs + 1)]

t = Int('total_time')  # end of schedule

solver = Optimize()

for i in range(1, njobs + 1):
    solver.add(start[i] >= 0)
    solver.add(end[i] <= t)
    solver.add(end[i] == start[i] + i + 10)

dependencies = {
    # Job 3 may only start if jobs 1 and 2 have been finished.
    3: [1, 2],
    # Job 6 may only start if jobs 2 and 4 have been finished.
    6: [2, 4],
    # Job 7 may only start if jobs 1, 4 and 5 have been finished.
    7: [1, 4, 5],
    # Job 8 may only start if jobs 3 and 6 have been finished.
    8: [3, 6],
    # Job 9 may only start if jobs 6 and 7 have been finished.
    9: [6, 7],
    # Job 10 may only start if jobs 8 and 9 have been finished.
    10: [8, 9],
}

for i, deps in dependencies.items():
    for d in deps:
        print (i, d)
        solver.add(start[i] >= end[d])

# 2. Take all requirements from Question 1, but now additionally it is
#    required that job 7 should not start earlier than job 8.
# Answer: 86
solver.add(start[7] >= start[8])


# 3. Take all requirements from Question 1 and Question 2, but now
#    additionally it is required that jobs 3, 4 and 5 are never allowed
#    to run at the same time, since they need a special equipment of
#    which only one copy is available.
# Answer: 98
for i in [3, 4, 5]:
    for j in [3, 4, 5]:
        if i != j:
            solver.add(Or(start[i] >= end[j], start[j] >= end[i]))


solver.minimize(t)
#import sys
#solver.add(t == int(sys.argv[1]))

result = solver.check()
print(result)

model = solver.model()
print(model)
print()

time = model.evaluate(t).as_long()
for i in range(1, njobs + 1):
    s = model.evaluate(start[i]).as_long()
    e = model.evaluate(end[i]).as_long()

    print("%2d:  ." % i, end="")

    last = False
    for t in range(1, time + 1):
        if t > s and t <= e:
            if not last or t == e:
                print(i if i != 10 else 0, end="")
            else:
                print("-", end="")
            last = True
        else:
            print(" ", end="")
            last = False
    print(".")
