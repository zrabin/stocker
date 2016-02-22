from tabulate import tabulate
import operator
from alg import Alg
import data


#data = rankings.getRankings(strategy="magic_formula_ttm")


companies = list(data.get_companies())                                      

companies = [c.symbol for c in companies]

data1 = Alg().getMagicFormulaTrailing()
data2 = Alg().getMagicFormulaFuture()
data3 = Alg().getGARP()

#data2 = Alg().getCompany(['AAPL', 'SSTK', 'CRM', 'DATA', 'GRMN'])
#data3 = Alg().getCompany(companies)

print tabulate(data1, headers="keys")
print tabulate(data2, headers="keys")
print tabulate(data3, headers="keys")
