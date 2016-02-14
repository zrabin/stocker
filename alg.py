#!/usr/bin/env python

from time import sleep 
import os
import database as d
import operator 


def magic_formula():
    # Score company pe_ttm
    query = d.Company.raw(
        '''SELECT company.symbol, 
        financialdata.rank_pe_ratio_ttm + financialdata.rank_return_on_assets AS magic_form_score_ttm,
        financialdata.rank_pe_ratio_ftm + financialdata.rank_return_on_assets AS magic_form_score_ftm
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
        mf_score_ttm = company.magic_form_score_ttm
        mf_score_ftm = company.magic_form_score_ftm
        values = []
        values.append(symbol)
        values.append(mf_score_ttm)
        values.append(mf_score_ftm)
        financials.append(values)

    return financials

