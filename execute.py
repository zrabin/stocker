from tabulate import tabulate
import operator
from alg import Alg


#data = rankings.getRankings(strategy="magic_formula_ttm")

data1 = Alg().getRankings('magic_formula_ttm')
data2 = Alg().getCompany('AAPL')

print tabulate(data1, headers="keys")
print tabulate(data2, headers="keys")

