#!/usr/bin/env python

import os 
import database

query = (
'''SELECT company.symbol, company.name, financialdata.pe_ratio_ttm
FROM company inner join financialdata
ON company.id = financialdata.company_id 
WHERE financialdata.pe_ratio_ttm > 0
ORDER BY company.symbol
DESC;'''
)

pe_ratio = database.db.execute_sql(query)

for i in pe_ratio:
    print i 

'''SELECT company.symbol, company.name, financialdata.pe_ratio_ttm 
FROM company inner join financialdata 
ON company.id = financialdata.company_id 
WHERE financialdata.pe_ratio_ttm > 0 
--ORDER BY financialdata.pe_ratio_ttm
ORDER BY company.symbol
DESC;'''

