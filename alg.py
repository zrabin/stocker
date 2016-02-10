#!/usr/bin/env python

from time import sleep 
import os
import database as d
import operator 

def set_rank(data):
    rank_pe_ttm = sorted(data, key=operator.itemgetter(2))
    rank_pe_ftm = sorted(data, key=operator.itemgetter(3))
    rank_pe_roa = sorted(data, key=operator.itemgetter(4))


def magic_formula():
    # Score company pe_ttm
    query = d.Company.raw(
        '''SELECT company.symbol, financialdata.pe_ratio_ttm, financialdata.return_on_assets,
        financialdata.ask / financialdata.EPSEstimateNextYear AS future_pe      
        FROM company 
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE financialdata.pe_ratio_ttm IS NOT Null 
        AND financialdata.return_on_assets IS NOT Null
        AND company.sector IS NOT 'Finance' 
        AND company.sector IS NOT 'Energy'
        AND company.sector IS NOT 'Miscellaneous'
        AND company.sector NOT LIKE '%Utilities%'
        ORDER BY company.symbol ASC'''
        )
    
    financials = []
    
    for company in query:
        symbol = company.symbol
        name = company.name 
        pe_ttm = company.pe_ratio_ttm
        pe_ftm = company.future_pe
        roa = company.return_on_assets
        values = []
        values.append(symbol)
        values.append(name)
        values.append(pe_ttm)
        values.append(pe_ftm)
        values.append(roa)
        financials.append(values)

    return financials

