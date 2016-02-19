from tabulate import tabulate
import operator
from alg import Alg


#data = rankings.getRankings(strategy="magic_formula_ttm")

data1 = Alg().getRankings('magic_formula_ttm')
data2 = Alg().getCompany(['AAPL', 'SSTK'])

print tabulate(data1, headers="keys")
print data2 

