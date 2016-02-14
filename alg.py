#!/usr/bin/env python

from time import sleep 
import os
import database as d
import operator 


def magic_formula():
    # Score company pe_ttm
    query = d.Company.raw(
        '''SELECT company.symbol, financialdata.rank_pe_ratio_ttm, financialdata.rank_return_on_assets,
        financialdata.rank_pe_ratio_ftm, financialdata.rank_pe_ratio_ftm + financialdata.rank_return_on_assets
        AS magic_form_score
        FROM company 
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE financialdata.rank_pe_ratio_ttm IS NOT Null 
        AND financialdata.rank_pe_ratio_ftm IS NOT Null 
        AND financialdata.rank_return_on_assets IS NOT Null
        AND company.sector IS NOT 'Finance' 
        AND company.sector IS NOT 'Energy'
        AND company.sector IS NOT 'Miscellaneous'
        AND company.sector NOT LIKE '%Utilities%'
        ORDER BY company.symbol ASC'''
        )
    
    financials = []
    
    for company in query:
        symbol = company.symbol
        pe_ttm = company.pe_ratio_ttm
        pe_ftm = company.pe_ratio_ftm
        roa = company.return_on_assets
        mf_score = company.magic_form_score
        values = []
        values.append(symbol)
        values.append(pe_ttm)
        values.append(pe_ftm)
        values.append(roa)
        values.append(mf_score)
        financials.append(values)

    return financials

