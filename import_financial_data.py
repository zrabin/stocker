#!/usr/bin/env python

import argparse
import bs4
import datetime
import logging
import re
import requests
import time
from bs4 import BeautifulSoup

import common
import data
import Quandl

QUAND_KEY = "1BCHxHp1ExoE4hXRmafE"
BATCH = 15
LOGGER = logging.getLogger('import_financial_data')
MONEY = { '': 10**3, 'M': 10**6, 'B': 10**9 }
MONEY_RE = re.compile(r'^\$?(\-?\d+\.?\d*)([MB])?$')


def get_month():
    now = datetime.datetime.now().date()
    return datetime.date(now.year, now.month, 1)

def check_valid(value):
    
    if value == 'N/A':
        return None

    if value is None:
        return value

    if isinstance(value, basestring):
        value = value.replace(',', '')
        return value
        
    return value

def decode_float(value):
    if isinstance(value, float):
        return value
    
    value = check_valid(value)

    if value is None:
        return value

    try:
        return float(value)
    except:
        print "could not convert value %s" % value
        return value


def decode_percent(value):
    value = check_valid(value)

    if value is None:
        return value

    percent = '%'
    if value.endswith(percent):
        value = value.strip(percent)

    return float(value)


def decode_money(value):
    value = check_valid(value)

    if not value:
        return None

    results = MONEY_RE.search(value)

    if not results:
        raise TypeError('invalid money: %s' % value)

    value = float(results.group(1))
    abbr = results.group(2) or ''

    return int(value * MONEY[abbr])

def decode_quandl(string):
    string = str(string)
    values = re.search(r'\d{4}.*', string)
    values = values.group()
    val_list = values.split(' ')
    return float(val_list[-1:])

def quandl_assets(sleep_time):
    month = get_month()

    companies = list(data.get_companies())

    for i, company in enumerate(companies):
        if i > 0: time.sleep(sleep_time)
        
        financials = []
        
        code_net_income = "RAYMOND/" + company.symbol + "_NET_INCOME_Q"
        code_total_assets = "RAYMOND/" + company.symbol + "_TOTAL_ASSETS_Q"
        
        try:
            net_income = Quandl.get(code_net_income, rows="1", authtoken=QUAND_KEY)
            net_income = decode_quandl(net_income)
            financials.append(["net_income", net_income])
        except:
            net_income = "N/A"
            financials.append(["net_income", net_income])
        
        try:
            total_assets = Quandl.get(code_total_assets, rows="1", authtoken=QUAND_KEY)
            total_assets = decode_quandl(total_assets)
            financials.append(["total_assets", total_assets])
        except:
            total_assets = "N/A"
            financials.append(["total_assets", total_assets])
        
        for key, value in financials:
            value = decode_float(value)
            print company.symbol, key, value 
            if key == "net_income":
                data.set_financial_data(
                    company=company, 
                    date=month,
                    net_income=value,
                    )
        
            elif key == "total_assets":
                data.set_financial_data(
                company=company, 
                date=month,
                total_assets=value,
                )


def yahoo_finance_quotes(sleep_time):
    month = get_month()

    companies = list(data.get_companies())
    companies = [companies[i:i+BATCH] for i in range(0, len(companies), BATCH)]

    for i, batch in enumerate(companies):
        if i > 0: time.sleep(sleep_time)

        batch = dict([(c.symbol, c) for c in batch])
        url = 'https://query.yahooapis.com/v1/public/yql'
        params = {
            'q': 'select * from yahoo.finance.quotes where symbol IN ("%s")' % '", "'.join(batch.keys()),
            'format': 'json',
            'env': 'http://datatables.org/alltables.env',
        }
        response = requests.get(url, params=params)
        body = response.json()

        LOGGER.info('Getting quotes: %s' % ', '.join(batch.keys()))

        for item in body['query']['results']['quote']:
            company = batch[item['symbol']]
            data.set_financial_data(
                company=company,
                date=month,
                ask=decode_money(item.get('Ask')),
                market_cap=decode_money(item.get('MarketCapitalization')),
                ebitda=decode_money(item.get('EBITDA')),
                pe_ratio_ttm=decode_float(item.get('PERatio')),
                peg_ratio=decode_float(item.get('PEGRatio')),
                eps_estimate_qtr=decode_float(item.get('EPSEstimateNextQuarter')),
                one_yr_target_price=decode_float(item.get('OneyrTargetPrice')),
                dividend_yield=decode_float(item.get('DividendYield')),
            )

def yahoo_finance_ks(sleep_time):
    month = get_month()
    url = 'https://finance.yahoo.com/q/ks'

    companies = list(data.get_companies())

    for i, company in enumerate(companies):
        if i > 0: time.sleep(sleep_time)

        LOGGER.info('Getting ks: %s' % company.symbol)

        map_data = {
            'Return on Assets (ttm):': {
                'key': 'return_on_assets',
                'decode': decode_percent,
            },
            'Return on Equity (ttm):': {
                'key': 'return_on_equity',
                'decode': decode_percent,
            },
        }

        response = requests.get(url, params={'s': company.symbol})
        soup = BeautifulSoup(response.text, 'html.parser')

        for doc in soup.body.find_all('tr'):
            try:
                md = map_data[doc.td.text]

                if doc.td.text in map_data:
                    md['value'] = doc.contents[1].text.strip()
            except:
                continue

        extra = {}

        for md in map_data.values():
            if 'value' not in md:
                continue
            value = md['decode'](md['value'])
            if value is not None:
                extra[md['key']] = value

        if extra:
            LOGGER.info('Setting ks: %s: %s' % (company.symbol, extra))
            data.set_financial_data(company=company, date=month, **extra)
        else:
            LOGGER.info('Skipping ks: %s' % company.symbol)



def main():
    common.setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument('--sleep-time', dest='sleep_time', type=float, default=1)

    subparsers = parser.add_subparsers()

    parser_yahoo_finance_quotes = subparsers.add_parser('yahoo_finance_quotes')
    parser_yahoo_finance_quotes.set_defaults(func=yahoo_finance_quotes)
    
    parser_quandl_assets = subparsers.add_parser('quandl_assets')
    parser_quandl_assets.set_defaults(func=quandl_assets)


#    parser_yahoo_finance_ks = subparsers.add_parser('yahoo_finance_ks')
#    parser_yahoo_finance_ks.set_defaults(func=yahoo_finance_ks)
    
    args = parser.parse_args()
    args.func(sleep_time=args.sleep_time)


if __name__ == '__main__':
    main()
