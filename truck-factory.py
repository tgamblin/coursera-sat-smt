#!/usr/bin/env python3
"""Filling trucks for a magic factory.

1. Eight trucks have to deliver pallets of obscure building blocks to a
   magic factory. Every truck has a capacity of 8000 kg and can carry at
   most eight pallets. In total, the following has to be delivered:

   - Four pallets of nuzzles, each of weight 800 kg.
   - A number of pallets of prittles, each of weight 1100 kg.
   - Eight pallets of skipples, each of weight 1000 kg.
   - Ten pallets of crottles, each of weight 2500 kg.
   - Twenty pallets of dupples, each of weight 200 kg.

   Skipples need to be cooled; only three of the eight trucks have the
   facility for cooling skipples.

   Nuzzles are very valuable; to distribute the risk of loss no two pallets
   of nuzzles may be in the same truck.

   Investigate what is the maximum number of pallets of prittles that can be
   delivered.

   (Hint: if you do not use the maximize command, you may run the tool
   several times and do a binary search to find the right value)


2. Consider all requirements from Question 1, but now with the following
   addtional requirement.

   - Prittles and crottles are an explosive combination: they are not
     allowed to be put in the same truck.

   Again, investigate what is the maximum number of pallets of prittles
   that can be delivered.

"""

from z3 import *

ntrucks = 8
nnuzzles = 4
nskipples = 8
ncrottles = 10
ndupples = 20

solver = Optimize()

# number of things
(nuzzles, prittles, skipples, crottles, dupples) = Ints(
    'nuzzles prittles skipples crottles dupples')

solver.add(nuzzles  == nnuzzles)
solver.add(skipples == nskipples)
solver.add(crottles == ncrottles)
solver.add(dupples  == ndupples)

# Counts of things in trucks
nuz_t = [Int('nuz_%d' % i) for i in range(ntrucks)]
pri_t = [Int('pri_%d' % i) for i in range(ntrucks)]
ski_t = [Int('ski_%d' % i) for i in range(ntrucks)]
cro_t = [Int('cro_%d' % i) for i in range(ntrucks)]
dup_t = [Int('dup_%d' % i) for i in range(ntrucks)]

pallets_t = [Int('pallets_%d' % i) for i in range(ntrucks)]

# function mapping truck to its weight
w = Function('w', IntSort(), IntSort())

# sum of things in trucks is number of things
solver.add(nuzzles  == Sum(*[nuz_t[i] for i in range(ntrucks)]))
solver.add(prittles == Sum(*[pri_t[i] for i in range(ntrucks)]))
solver.add(skipples == Sum(*[ski_t[i] for i in range(ntrucks)]))
solver.add(crottles == Sum(*[cro_t[i] for i in range(ntrucks)]))
solver.add(dupples  == Sum(*[dup_t[i] for i in range(ntrucks)]))

# can't have negative things in trucks
for t in range(ntrucks):
    solver.add(nuz_t[t] >= 0)
    solver.add(pri_t[t] >= 0)
    solver.add(ski_t[t] >= 0)
    solver.add(cro_t[t] >= 0)
    solver.add(dup_t[t] >= 0)

for i in range(ntrucks):
    # no truck can have more than 8000 kg
    solver.add(w(i) <= 8000)

    solver.add(pallets_t[i] == Sum(
        nuz_t[i], pri_t[i], ski_t[i], cro_t[i], dup_t[i]))

    # no more than 8 pallets per truck
    solver.add(pallets_t[i] <= 8)

    # truck's weight is the sum of its cargo
    solver.add(
        w(i) == Sum(
            nuz_t[i] * 800,
            pri_t[i] * 1100,
            ski_t[i] * 1000,
            cro_t[i] * 2500,
            dup_t[i] * 200,
        )
    )

    # can't have prittles and crottles in same truck
    solver.add(Not(And(pri_t[i] > 0, cro_t[i] > 0)))

    # no two nuzzles in the same truck
    solver.add(nuz_t[i] <= 1)

    # only (first) 3 trucks can carrry skipples
    if i >= 3:
        solver.add(ski_t[i] == 0)


solver.maximize(prittles)
result = solver.check()
print(result)

m = solver.model()
print(m)
