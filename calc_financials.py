#!/usr/bin/env python

import argparse
import datetime
import time
import logging
import common
import data
import alg
import database as d

#LOGGER = logging.getLogger('import_financial_data')
#MONEY = { '': 10**3, 'M': 10**6, 'B': 10**9 }
#MONEY_RE = re.compile(r'^\$?(\-?\d+\.?\d*)([MB])?$')

def get_time():
    now = datetime.date.today()
    return now

def calc_pe_ratio_ftm():
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
   
    for x in financials:
        print "setting %s --- pe_ratio_ftm = %s" % (x['symbol'], x['pe_ratio_ftm'])
        data.set_financial_data(
            company=x["company"],
            symbol=x["symbol"],
            date=get_time(),
            pe_ratio_ftm=x["pe_ratio_ftm"]
        )

    return financials



def rank_financials():
    attributes = {
#        "ask" : "desc",
#        "book_value" : "desc",
#        "market_cap" : "desc",
        "ebitda" : "desc",
        "pe_ratio_ttm" : "asc",
        "pe_ratio_ftm" : "asc",
        "eps_estimate_qtr" : "desc",
        "peg_ratio" : "asc",
        "return_on_assets" : "desc",
        "return_on_equity" : "desc",
        "change_year_low_per" : "desc",
        "change_year_high_per" : "desc",
#        "net_income" : "desc",
#        "total_assets" : "desc",
#        "OneyrTargetPrice" : "desc",
        "DividendYield" : "desc",
#        "EPSEstimateCurrentYear" : "desc",
#        "EPSEstimateNextYear" : "desc",
#        "EPSEstimateNextQuarter" : "desc"
    }

    for f in attributes.keys():
        if attributes[f] == "asc":
            query = d.FinancialData.select(
                d.FinancialData.symbol,
                getattr(d.FinancialData, f)).where(
                getattr(d.FinancialData, f).is_null(False)).order_by(
                getattr(d.FinancialData, f))
        elif attributes[f] == "desc":
            query = d.FinancialData.select(
                d.FinancialData.symbol,
                getattr(d.FinancialData, f)).where(
                getattr(d.FinancialData, f).is_null(False)).order_by(
                getattr(d.FinancialData, f).desc())
        
        #    getattr(d.FinancialData, f)
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
            print "Setting %s rank for %s to %s" % (field, company, rank)
            data.set_rank(company, date, field, rank)

    
def main():

#    calc_pe_ratio_ftm()
    
    rank_financials()


if __name__ == '__main__':
    main()
