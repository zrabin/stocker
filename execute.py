import operator 
import alg

mf = alg.magic_formula()

rank_future = sorted(mf, key=operator.itemgetter(1))

for rank, data in enumerate(rank_future):
    print rank, data
