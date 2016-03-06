#!/usr/bin/env python

from time import sleep 
import os
import database as d
import operator 
import data
    
    
def getRank(model, strategy):

    financials = []
    strategy = strategy

    rank = 0 
    for company in model:
        rank = rank + 1
        symbol = company.symbol
        score = company.score
        values = {}
        values.update({"company" : company})
        values.update({"rank" : rank})
        values.update({"symbol" : symbol})
        values.update({strategy : score})
        financials.append(values)

    financials = sorted(financials, key=operator.itemgetter("rank"))

    return financials

class Alg(object):
    
    def toList(self, arg):
        if not isinstance(arg, (list, tuple)):
            arg = [arg]
        return arg

    
    def __init__(self):
        companies = list(data.get_companies())
        self.companies = [c.symbol for c in companies]
        self.strategies = [
            "magic_formula_ttm",
            "magic_formula_ftm",
            "garp_ratio"
            ]
    
    
    def calcMagicFormulaTrailing(self, companies=None):
        
        strategy = "magic_formula_ttm"
        
        query = d.Company.raw(
            '''SELECT company.symbol, 
            financialdata.rank_pe_ratio_ttm + financialdata.rank_return_on_assets AS score
            FROM company 
            INNER JOIN financialdata on company.id = financialdata.company_id
            WHERE financialdata.rank_pe_ratio_ttm IS NOT Null 
            AND financialdata.rank_return_on_assets IS NOT Null
            AND company.sector IS NOT 'Finance' 
            AND company.sector IS NOT 'Energy'
            AND company.sector IS NOT 'Miscellaneous'
            AND company.sector NOT LIKE '%Utilities%'
            ORDER BY score ASC'''
            )

        rankings = getRank(query, strategy)

        return rankings
    
    
    def calcMagicFormulaFuture(self, companies=None):
        
        strategy = "magic_formula_ftm"
        
        query = d.Company.raw(
            '''SELECT company.symbol, 
            financialdata.rank_pe_ratio_ftm + financialdata.rank_return_on_assets AS score
            FROM company 
            INNER JOIN financialdata on company.id = financialdata.company_id
            AND financialdata.rank_pe_ratio_ftm IS NOT Null 
            AND financialdata.rank_return_on_assets IS NOT Null
            AND company.sector IS NOT 'Finance' 
            AND company.sector IS NOT 'Energy'
            AND company.sector IS NOT 'Miscellaneous'
            AND company.sector NOT LIKE '%Utilities%'
            ORDER BY score ASC'''
            )
        
        rankings = getRank(query, strategy)

        return rankings

    def calcGARP(self, companies=None):
        
        strategy = "GARP"
        
        query = d.Company.raw(
            '''SELECT company.symbol, 
            financialdata.garp_ratio AS score
            FROM company 
            INNER JOIN financialdata on company.id = financialdata.company_id
            WHERE financialdata.garp_ratio > 0 
            AND company.sector IS NOT 'Finance' 
            AND company.sector IS NOT 'Energy'
            AND company.sector IS NOT 'Miscellaneous'
            AND company.sector NOT LIKE '%Utilities%'
            ORDER BY score ASC'''
            )
        
        rankings = getRank(query, strategy)

        return rankings
                
    
