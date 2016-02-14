import operator 
import alg

mf = alg.magic_formula()

rank_future = sorted(mf, key=operator.itemgetter(2))

for rank, data in enumerate(rank_future):
    print rank, data
