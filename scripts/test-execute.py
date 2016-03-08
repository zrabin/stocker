from tabulate import tabulate
import operator
from alg import Alg
import data


companies = list(data.get_companies())                                      

companies = [c.symbol for c in companies]

data1 = Alg().getMagicFormulaTrailing()
data2 = Alg().getMagicFormulaFuture()
data3 = Alg().getGARP()

#data2 = Alg().getCompany(['AAPL', 'SSTK', 'CRM', 'DATA', 'GRMN'])
#data3 = Alg().getCompany(companies)

print data4
#print tabulate(data4, headers="keys")
#print tabulate(data1, headers="keys")
#print tabulate(data2, headers="keys")
#print tabulate(data3, headers="keys")
