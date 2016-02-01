#!/usr/bin/env python

from time import sleep 
import os
import database as d
import operator 

def tech_magic_formula():
    # Score company pe_ttm
    tech_pe_ttm = (d.Company.raw(
        '''SELECT company.symbol, financialdata.pe_ratio_ttm
        FROM company 
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE financialdata.pe_ratio_ttm is not Null 
        AND company.sector LIKE 'Technology'
        ORDER BY financialdata.pe_ratio_ttm ASC'''
        ))
    
    pe_score = {}
    for rank, company in enumerate(tech_pe_ttm):
        pe_score.update({company.symbol : rank})
    
    
    # Score company ROA
    tech_roa = (d.Company.raw(
        '''SELECT company.symbol, financialdata.return_on_assets
        FROM company 
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE financialdata.return_on_assets is not Null 
        AND company.sector LIKE 'Technology'
        ORDER BY financialdata.return_on_assets DESC'''
        ))
    
    roa_score = {}
    for rank, company in enumerate(tech_roa):
        roa_score.update({company.symbol : rank})
    
    
    # Combine scores
    score = {}
    for i in pe_score.keys():
        if i in roa_score:
            combined = pe_score[i] + roa_score[i]
            score.update({i : combined})
   
    sorted_score = sorted(score.items(), key=operator.itemgetter(1))

    return sorted_score
        
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
#    query = d.Company.raw(
#        '''SELECT company.symbol, financialdata.pe_ratio_ttm, financialdata.return_on_assets,
#        financialdata.ask / financialdata.EPSEstimateNextYear AS future_pe      
#        FROM company 
#        INNER JOIN financialdata on company.id = financialdata.company_id
#        WHERE financialdata.pe_ratio_ttm IS NOT Null 
#        AND financialdata.return_on_assets IS NOT Null
#        AND company.sector IS NOT 'Finance' 
#        AND company.sector IS NOT 'Energy'
#        AND company.sector IS NOT 'Miscellaneous'
#        AND company.sector NOT LIKE '%Utilities%'
#        ORDER BY company.symbol ASC'''
#        )
   
    print query
    financials = {}
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
        financials.update({symbol : values})

    
#    roa_score = {}
#    for rank, company in enumerate(roa):
#        roa_score.update({company.symbol : rank})
#    
#    # Combine scores
#    score = {}
#    for i in pe_score.keys():
#        if i in roa_score:
#            combined = pe_score[i] + roa_score[i]
#            score.update({i : combined})
#   
#    sorted_score = sorted(score.items(), key=operator.itemgetter(1))

    return financials
        
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
    roa = (d.Company.raw(
        '''SELECT company.symbol, financialdata.return_on_assets
        FROM company 
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE financialdata.return_on_assets is not Null 
        AND company.sector IS NOT 'Finance' 
        AND company.sector IS NOT 'Energy'
        AND company.sector IS NOT 'Miscellaneous'
        AND company.sector NOT LIKE '%Utilities%'
        ORDER BY financialdata.return_on_assets DESC'''
        ))
    
    roa_score = {}
    for rank, company in enumerate(roa):
        roa_score.update({company.symbol : rank})
    
    
    score = {}
    for i in pe_score.keys():
        if i in roa_score:
            combined = pe_score[i] + roa_score[i]
            score.update({i : combined})
   
    sorted_score = sorted(score.items(), key=operator.itemgetter(1))
    output = []
    
    for pair in sorted_score:
        c = pair[0]
        sql = (d.Company.raw(
            '''SELECT company.name, company.symbol, financialdata.return_on_assets,
            financialdata.Ask / financialdata.EPSEstimateNextYear AS future_pe
            FROM company
            INNER JOIN financialdata on company.id = financialdata.company_id       
            AND financialdata.return_on_assets is not Null
            AND future_pe IS NOT Null
            AND company.sector IS NOT 'Finance' 
            AND company.sector IS NOT 'Energy'
            AND company.sector IS NOT 'Miscellaneous'
            AND company.sector NOT LIKE '%Utilities%' '''))
        print c 
        sleep(2)
        for obj in sql:
            print "looping"
            print obj

            print obj.symbol, obj.name
            raw_input("Press Enter to continue...")

            output.append(company.name, company.symbol, financialdata.return_on_assets)

    return output
        
## Score company ROA
#    roa = (d.Company
#            .select(d.Company.name, d.Company.symbol, d.FinancialData.return_on_assets)
#            .join(d.FinancialData, on=(d.FinancialData.company_id == d.Company))
#            .where((d.Company.sector != 'Finance') & (d.Company.sector != 'Energy') 
#            & (d.Company.sector != 'Miscellaneous') & (d.Company.sector != '%Utilities%')
#            & (d.FinancialData.return_on_assets != None)) 
#            .order_by(d.FinancialData.return_on_assets)
#        )
