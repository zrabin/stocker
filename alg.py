#!/usr/bin/env python

import os
import database as d
import operator 

def tech_50_ranked_pe_ratio():
    sql = (d.Company
                .select(d.Company.name, d.Company.symbol, d.FinancialData.pe_ratio_ttm)
                .join(d.FinancialData, on=(d.Company == d.FinancialData.company_id))
                .where((d.Company.sector == 'Technology') & (d.FinancialData.pe_ratio_ttm != None))
                .order_by(d.FinancialData.pe_ratio_ttm)
            )
    
    score = {}
    for rank, company in enumerate(sql):
        score.update({company.symbol : rank})
    
    return score
        
def tech_50_ranked_roa():
    sql = (d.Company
            .select(d.Company.name, d.Company.symbol, d.FinancialData.return_on_assets)
            .join(d.FinancialData, on=(d.FinancialData.company_id == d.Company))
            .where((d.Company.sector == 'Technology') & (d.FinancialData.return_on_assets != None))
            .order_by(d.FinancialData.return_on_assets.desc())
            )
    
    score = {}
    for rank, company in enumerate(sql):
        score.update({company.symbol : rank})
    
    return score

def magic_50():
    pe = tech_50_ranked_pe_ratio()
    roa = tech_50_ranked_roa()

    score = {}
    for i in pe.keys():
        if i in roa:
            combined = pe[i] + roa[i]
            score.update({i : combined})
   
    sorted_score = sorted(score.items(), key=operator.itemgetter(1))

    return sorted_score

print magic_50()
