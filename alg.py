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
        
def tech_50_ranked_eps_estimate_qtr():
    sql = (d.Company
                .select(d.Company.name, d.Company.symbol, d.FinancialData.eps_estimate_qtr)
                .join(d.FinancialData, on=(d.Company == d.FinancialData.company_id))
                .where((d.Company.sector == 'Technology') & (d.FinancialData.eps_estimate_qtr != None))
                .order_by(d.FinancialData.pe_ratio_ttm)
            )
    
    score = {}
    for rank, company in enumerate(sql):
        score.update({company.symbol : rank})
    
    return score

def tech_50_ranked_price():
    sql = (d.Company
                .select(d.Company.name, d.Company.symbol, d.FinancialData.ask)
                .join(d.FinancialData, on=(d.Company == d.FinancialData.company_id))
                .where((d.Company.sector == 'Technology') & (d.FinancialData.eps_estimate_qtr != None))
                .order_by(d.FinancialData.ask)
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

def magic_50_future():
    pe = tech_50_ranked_pe_ratio()
    future_eps = tech_50_ranked_eps_estimate_qtr()
    price = tech_50_ranked_price()
    roa = tech_50_ranked_roa()

    f_pe = {}
    for i in price.keys():
        if i in future_eps:
            try:
                future_pe = price[i] / future_eps[i]
                f_pe.update({i : future_pe})
            except:
                continue
    
    score = {}
    for i in f_pe.keys():
        if i in roa:
            combined = f_pe[i] + roa[i]
            score.update({i : combined})
   
    sorted_score = sorted(score.items(), key=operator.itemgetter(1))

    return sorted_score

print magic_50()
