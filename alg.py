#!/usr/bin/env python

from time import sleep 
import os
import database as d
import operator 

class Alg(object):
    
    def toList(self, arg):
        if not isinstance(arg, (list, tuple)):
            arg = [arg]
        return arg


    strategies =[ 
        "magic_formula_ttm",
        "magic_formula_ftm",
    ]
    
    def __init__(self):
        return

    def getRankings(self, strategy):
        
        strategies =[ 
            "magic_formula_ttm",
            "magic_formula_ftm",
            ]

        if strategy == "magic_formula_ttm":

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
        
        elif strategy == "magic_formula_ftm":

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
        
        else:
            return "That's not a valid strategy %s" % strategies

        financials = []
        rank = 0 
        for company in query:
            rank = rank + 1
            symbol = company.symbol
            score = company.score
            values = {}
            values.update({"rank" : rank})
            values.update({"symbol" : symbol})
            values.update({strategy : score})
            financials.append(values)

        financials = sorted(financials, key=operator.itemgetter("rank"))

        return financials

    def getCompany(self, arg):
        
        companies = Alg().toList(arg)

        strategies = Alg.strategies
            
        data = []    
        
        for company in companies:
            values = {}
            values.update({"symbol" : company})

            for strategy in strategies:
                rank = Alg().getRankings(strategy)
                
                for x in rank:
                    
                    if x["symbol"] != company:
                        continue
                    
                    elif x["symbol"] == company:
                        score = {strategy : x["rank"]}
                        values.update(score)

                    else:
                        values.update({"error" : "could not find that ticker"})
                    
                    data.append(values)
 
        return data

                        
                        





            

