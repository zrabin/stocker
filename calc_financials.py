#!/usr/bin/env python

import argparse
import datetime
import time
import logging
import common
import data
import alg
import database as d

LOGGER = logging.getLogger('calc_financials')

def get_time():
    now = datetime.date.today()
    return now

def calc_pe_ratio_ftm():
    
    LOGGER.info('Calculating pe ratio')

    query = d.Company.raw(
        '''SELECT company.symbol, 
        financialdata.ask / financialdata.EPSEstimateNextYear AS future_pe      
        FROM company 
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE financialdata.ask IS NOT Null 
        AND financialdata.EPSEstimateNextYear IS NOT Null
        ORDER BY company.symbol ASC'''
        )
    
    financials = []
    
    for row in query:
        symbol = row.symbol
        pe_ratio_ftm = row.future_pe
        values = {}
        values.update({
            "company" : row.id, 
            "symbol" : symbol,
            "pe_ratio_ftm" : pe_ratio_ftm
        })
        financials.append(values)
  
    count = 0
    for x in financials:
        count = count + 1
        data.set_financial_data(
            company=x["company"],
            symbol=x["symbol"],
            date=get_time(),
            pe_ratio_ftm=x["pe_ratio_ftm"]
        )

    LOGGER.info('Finished calculating pe_ratio - %s total calculations' % count)
    return financials


def calc_garp_ratio():
    
    LOGGER.info('Calculating garp ratio')
    
    query = d.Company.raw(
        '''SELECT company.symbol, 
        financialdata.pe_ratio_ttm / financialdata.peg_ratio as garp_ratio  
        FROM company 
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE financialdata.pe_ratio_ttm IS NOT Null 
        AND financialdata.peg_ratio IS NOT Null
        ORDER BY company.symbol ASC'''
        )
    
    financials = []
    
    for row in query:
        symbol = row.symbol
        garp_ratio = row.garp_ratio
        values = {}
        values.update({
            "company" : row.id, 
            "symbol" : symbol,
            "garp_ratio" : garp_ratio
        })
        financials.append(values)
    
    count = 0
    for x in financials:
        count = count + 1
        data.set_financial_data(
            company=x["company"],
            symbol=x["symbol"],
            date=get_time(),
            garp_ratio=x["garp_ratio"]
        )
    
    LOGGER.info('Finished calculating garp_ratio - %s total calculations' % count)


def calc_magic_formula_trailing():
    
    LOGGER.info('Calculating Magic Formula Trailing')
    
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

    rankings = alg.getRank(query, strategy)
    count = 0
    for x in rankings:
        count = count + 1
        data.set_financial_data(
            company = x["company"],
            symbol = x["symbol"],
            date=get_time(),
            magic_formula_trailing = x[strategy]
        )
    
    LOGGER.info('Finished calculating Magic F Trailing - %s total calculations' % count)


def calc_magic_formula_future():
    
    LOGGER.info('Calculating Magic Formula Future')
    
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
   
    rankings = alg.getRank(query, strategy)
    count = 0
    for x in rankings:
        count = count + 1
        data.set_financial_data(
            company = x["company"],
            symbol = x["symbol"],
            date=get_time(),
            magic_formula_future = x[strategy]
        )
    
    LOGGER.info('Finished calculating Magic F Future - %s total calculations' % count)


def calc_ranks():
    
    attributes = {
#        "ask" : "desc",
#        "book_value" : "desc",
#        "market_cap" : "desc",
        "ebitda" : "desc",
        "pe_ratio_ttm" : "asc",
        "pe_ratio_ftm" : "asc",
        "eps_estimate_qtr" : "desc",
        "peg_ratio" : "asc",
        "garp_ratio" : "asc",
        "return_on_assets" : "desc",
        "return_on_equity" : "desc",
        "change_year_low_per" : "desc",
        "change_year_high_per" : "desc",
        "magic_formula_trailing" : "asc",
        "magic_formula_future" : "asc",
#        "net_income" : "desc",
#        "total_assets" : "desc",
#        "OneyrTargetPrice" : "desc",
        "DividendYield" : "desc",
#        "EPSEstimateCurrentYear" : "desc",
#        "EPSEstimateNextYear" : "desc",
#        "EPSEstimateNextQuarter" : "desc"
    }

    LOGGER.info('Calculating Ranks for %s' % attributes.keys())
    
    for f in attributes.keys():
        if attributes[f] == "asc":
            LOGGER.info('Calculating %s %s' % (f, attributes[f]))
            
            query = d.FinancialData.select(
                d.FinancialData.symbol,
                getattr(d.FinancialData, f)).where(
                getattr(d.FinancialData, f).is_null(False)).order_by(
                getattr(d.FinancialData, f))
        
        elif attributes[f] == "desc":
            LOGGER.info('Calculating %s %s' % (f, attributes[f]))
            
            query = d.FinancialData.select(
                d.FinancialData.symbol,
                getattr(d.FinancialData, f)).where(
                getattr(d.FinancialData, f).is_null(False)).order_by(
                getattr(d.FinancialData, f).desc())
        
        financial_data = []
	
	for rank, row in enumerate(query):
            company = row.symbol
            field = "rank_" + f
            rank = rank + 1
            financial_data.append({"company" : company, "field" : field, "rank" : rank})

        for key in financial_data:
            company = key["company"]
            field = key["field"]
            rank = key["rank"]
            date = get_time()
            data.set_rank(company, date, field, rank)
    
def main():

    common.setup_logging()

    calc_pe_ratio_ftm()
    calc_garp_ratio()
    calc_magic_formula_trailing() 
    calc_magic_formula_future() 
    calc_ranks()

if __name__ == '__main__':
    main()
