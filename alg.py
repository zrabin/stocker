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
                
    
#    def getRankings(self, strategy):
#        
#        alg = Alg()
#        strategies = self.strategies
#
#        if strategy == "magic_formula_ttm":
#            return alg.getMagicFormulaTrailing()
#        
#        elif strategy == "garp_ratio":
#            return alg.getGARP()
#        
#        elif strategy == "magic_formula_ftm":
#            return alg.getMagicFormulaFuture()
#        
#        elif strategy == "all":
#            
#            magic_formula_future = alg.getMagicFormulaFuture(),
#            magic_formula_trailing  = alg.getMagicFormulaTrailing(),
#            garp = alg.getGARP()
#            
#            rankings = {
#            "magic_formula_future" : magic_formula_future,
#            "magic_formula_trailing" : magic_formula_trailing,
#            "garp" : garp
#            }
#            
#            return rankings
#
#        else:
#            return "That's not a valid strategy %s" % strategies
#
#
#    def getCompany(self, company):
#        
#        companies = Alg().toList(company)
#        strategies = self.strategies
#        
#        data = []
#        for company in companies:
#            values = {}
#            values.update({"symbol" : company})
#
#            for strategy in strategies:
#                rank = Alg().getRankings(strategy)
#                
#                for x in rank:
#                    if x["symbol"] != company:
#                        continue
#                    
#                    elif x["symbol"] == company:
#                        score = {strategy : x["rank"]}
#                        values.update(score)
#
#                    else:
#                        values.update({"error" : "could not find that ticker"})
#                    
#                    data.append(values)
# 
#        return data

