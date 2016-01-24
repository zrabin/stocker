#!/usr/bin/env python

import os
import database as d



def tech_50_ranked_pe_ratio():
    sql = (d.Company
                .select(d.Company.name, d.Company.symbol, d.FinancialData.pe_ratio_ttm)
                .join(d.FinancialData, on=(d.Company == d.FinancialData.company_id))
                .where(d.Company.sector == 'Technology')
                .order_by(d.FinancialData.pe_ratio_ttm)
            )
    return sql


def tech_50_ranked_roa():
    sql = (d.Company
            .select(d.Company.name, d.Company.symbol, d.FinancialData.return_on_assets)
            .join(d.FinancialData, on=(d.FinancialData.company_id == d.Company))
            .where(d.Company.sector == 'Technology')
            .order_by(d.FinancialData.return_on_assets)
            )
    return sql


for rank, i in enumerate(tech_50_ranked_roa()):
    print rank, i.name, i.symbol, i.financialdata.return_on_assets

#for obj in tech_50_ranked_pe_ratio():
#    for a, b, c in obj:
#        print a


#def test():
#    return (d.Company
#            .select())
#


#query = (
#'''SELECT company.symbol, company.name, financialdata.pe_ratio_ttm
#FROM company inner join financialdata
#ON company.id = financialdata.company_id 
#WHERE financialdata.pe_ratio_ttm > 0
#ORDER BY company.symbol
#DESC;'''
#)
#
#pe_ratio = database.db.execute_sql(query)
#
#for i in pe_ratio:
#    print i 
#
#'''SELECT company.symbol, company.name, financialdata.pe_ratio_ttm 
#FROM company inner join financialdata 
#ON company.id = financialdata.company_id 
#WHERE financialdata.pe_ratio_ttm > 0 
#--ORDER BY financialdata.pe_ratio_ttm
#ORDER BY company.symbol
#DESC;'''
#
