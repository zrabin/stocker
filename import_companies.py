#!/usr/bin/env python

import StringIO
import csv
import requests

import data


EXCHANGES = ('nasdaq', 'nyse', 'amex')


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
    for exchange in EXCHANGES:
        for company in get_companies(exchange):
            data.set_company(
                symbol=company.symbol,
                name=company.name,
                sector=company.sector,
                industry=company.industry,
            )


if __name__ == '__main__':
    main()
