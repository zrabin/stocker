#!/usr/bin/env python

import StringIO
import argparse
import csv
import logging
import requests
import common
import data

####
# Setup tor to use for all imports
import socks
import socket 
import requests

#socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr="127.0.0.1", port=9050)
#socket.socket = socks.socksocket
#####

EXCHANGES = ('nasdaq', 'nyse', 'amex')
LOGGER = logging.getLogger('import_companies')


class Company(object):

    def __init__(self, symbol=None, name=None, market_cap=None, sector=None, industry=None):
        self.symbol = symbol
        self.name = name
        self.market_cap = market_cap
        self.sector = sector
        self.industry = industry

    def __str__(self):
        return 'Company(symbol=%s, name=%s, market_cap=%s, sector=%s, industry=%s)' % (
            self.symbol, self.name, self.market_cap, self.sector, self.industry)

    @staticmethod
    def decode_value(value):
        value = value.strip()

        if value == '' or value == 'n/a':
            return None

        return value

    @staticmethod
    def decode_int(value):
        value = Company.decode_value(value)

        if value is None:
            return value

        return int(value)

    @staticmethod
    def decode(row):
        return Company(
            symbol=Company.decode_value(row[0]),
            name=Company.decode_value(row[1]),
            sector=Company.decode_value(row[5]),
            industry=Company.decode_value(row[6])
        )


def get_companies(exchange):
    companies = []

    url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?exchange=%s&render=download' % exchange
    response = requests.get(url)

    reader = csv.reader(StringIO.StringIO(response.text))

    for i, row in enumerate(reader):
        if i == 0: continue
        companies.append(Company.decode(row))

    return companies


def main():
    common.setup_logging()

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    for exchange in EXCHANGES:
        LOGGER.info('Getting exchange: %s' % exchange)

        for company in get_companies(exchange):
            data.set_company(
                symbol=company.symbol,
                name=company.name,
                sector=company.sector,
                industry=company.industry,
            )


if __name__ == '__main__':
    main()
