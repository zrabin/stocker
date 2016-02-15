from tabulate import tabulate
import operator
from alg import Alg

rankings = Alg()

data = rankings.getRankings(strategy="magic_formula_ttm")

print tabulate(data, headers="keys")

#for rank, data in enumerate(rank_future):
#    url = "https://www.google.com/finance?q="
#    print rank, tabulate(data), url + str(data["symbol"]) 
