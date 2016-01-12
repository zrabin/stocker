#!/usr/bin/env python

import argparse
import datetime
import logging
import re
import requests
import time

import common
import data


BATCH = 50
LOGGER = logging.getLogger('import_finance')
MONEY = { '': 10**3, 'M': 10**6, 'B': 10**9 }
MONEY_RE = re.compile(r'^\$?(\-?\d+\.?\d*)([MB])?$')


def decode_float(item, name):
    value = item.get(name)

    if value is None:
        return value

    return float(value)


def decode_money(item, name):
    value = item.get(name)

    if not value:
        return None

    results = MONEY_RE.search(value)

    if not results:
        raise TypeError('invalid money: %s' % value)

    value = float(results.group(1))
    abbr = results.group(2) or ''

    return int(value * MONEY[abbr])



def main(sleep_time):
    now = datetime.datetime.now().date()
    first_of_month = datetime.date(now.year, now.month, 1)

    companies = list(data.get_companies())
    companies = [companies[i:i+BATCH] for i in range(0, len(companies), BATCH)]

    for batch in companies:
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
                date=first_of_month,
                market_cap=decode_money(item, 'MarketCapitalization'),
                ebitda=decode_money(item, 'EBITDA'),
                pe_ratio=decode_float(item, 'PERatio'),
                peg_ratio=decode_float(item, 'PERatio'),
                one_yr_target_price=decode_float(item, 'OneyrTargetPrice'),
                dividend_yield=decode_float(item, 'DividendYield'),
            )

        time.sleep(sleep_time)


if __name__ == '__main__':
    common.setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument('--sleep-time', dest='sleep_time', type=float, default=1)

    args = parser.parse_args()

    main(sleep_time=args.sleep_time)
