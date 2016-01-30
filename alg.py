#!/usr/bin/env python

import os
import database as d
import operator 

def tech_magic_formula():
    # Score company pe_ttm
    tech_pe_ttm = (d.Company
                .select(d.Company.name, d.Company.symbol, d.FinancialData.pe_ratio_ttm)
                .join(d.FinancialData, on=(d.Company == d.FinancialData.company_id))
                .where((d.Company.sector == 'Technology') & (d.FinancialData.pe_ratio_ttm != None))
                .order_by(d.FinancialData.pe_ratio_ttm)
            )
    
    pe_score = {}
    for rank, company in enumerate(tech_pe_ttm):
        pe_score.update({company.symbol : rank})
    
    
    # Score company ROA
    tech_roa = (d.Company
            .select(d.Company.name, d.Company.symbol, d.FinancialData.return_on_assets)
            .join(d.FinancialData, on=(d.FinancialData.company_id == d.Company))
            .where((d.Company.sector == 'Technology') & (d.FinancialData.return_on_assets != None))
            .order_by(d.FinancialData.return_on_assets.desc())
            )
    
    roa_score = {}
    for rank, company in enumerate(tech_roa):
        roa_score.update({company.symbol : rank})
    
    
    score = {}
    for i in pe_score.keys():
        if i in roa_score:
            combined = pe_score[i] + roa_score[i]
            score.update({i : combined})
   
    sorted_score = sorted(score.items(), key=operator.itemgetter(1))

    return sorted_score
        
def magic_formula():
    # Score company pe_ttm

    pe_ttm = (d.Company
                .select(d.Company.name, d.Company.symbol, d.FinancialData.pe_ratio_ttm)
                .join(d.FinancialData, on=(d.Company == d.FinancialData.company_id))
                .where((d.Company.sector != 'Finance') & (d.Company.sector != 'Energy') 
                & (d.Company.sector != 'Miscellaneous') & (d.Company.sector != '%Utilities%') 
                & (d.FinancialData.pe_ratio_ttm != None))
                .order_by(d.FinancialData.pe_ratio_ttm)
            )
    
    pe_score = {}
    for rank, company in enumerate(pe_ttm):
        pe_score.update({company.symbol : rank})
    
    
    # Score company ROA
    roa = (d.Company
            .select(d.Company.name, d.Company.symbol, d.FinancialData.return_on_assets)
            .join(d.FinancialData, on=(d.FinancialData.company_id == d.Company))
            .where((d.Company.sector != 'Finance') & (d.Company.sector != 'Energy') 
            & (d.Company.sector != 'Miscellaneous') & (d.Company.sector != '%Utilities%')
            & (d.FinancialData.return_on_assets != None)) 
            .order_by(d.FinancialData.return_on_assets)
        )
    
    roa_score = {}
    for rank, company in enumerate(roa):
        roa_score.update({company.symbol : rank})
    
    
    score = {}
    for i in pe_score.keys():
        if i in roa_score:
            combined = pe_score[i] + roa_score[i]
            score.update({i : combined})
   
    sorted_score = sorted(score.items(), key=operator.itemgetter(1))

    return sorted_score
        
def magic_formula_future():
    # Score company pe_ttm

    pe_future = (d.Company.raw(
        '''SELECT company.symbol, 
        financialdata.Ask / financialdata.EPSEstimateNextYear AS future_pe
        FROM company inner join financialdata on company.id = financialdata.company_id
        WHERE future_pe is not Null 
        AND company.sector is not 'Finance' 
        AND company.sector is not 'Energy'
        AND company.sector is not 'Miscellaneous'
        AND company.sector not like '%Utilities%'
        ORDER BY future_pe ASC'''
        ))
    
    pe_score = {}
    for rank, company in enumerate(pe_future):
        pe_score.update({company.symbol : rank})
    
    
    # Score company ROA
    roa = (d.Company
            .select(d.Company.name, d.Company.symbol, d.FinancialData.return_on_assets)
            .join(d.FinancialData, on=(d.FinancialData.company_id == d.Company))
            .where((d.Company.sector != 'Finance') & (d.Company.sector != 'Energy') 
            & (d.Company.sector != 'Miscellaneous') & (d.Company.sector != '%Utilities%')
            & (d.FinancialData.return_on_assets != None)) 
            .order_by(d.FinancialData.return_on_assets)
        )
    
    roa_score = {}
    for rank, company in enumerate(roa):
        roa_score.update({company.symbol : rank})
    
    
    score = {}
    for i in pe_score.keys():
        if i in roa_score:
            combined = pe_score[i] + roa_score[i]
            score.update({i : combined})
   
    sorted_score = sorted(score.items(), key=operator.itemgetter(1))

    return sorted_score
        

print magic_formula_future()
