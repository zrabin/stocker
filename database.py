#!/usr/bin/env python

import os

from peewee import *
from playhouse import db_url


db = db_url.connect(os.environ.get('DATABASE_URL', 'sqlite:///stocker.db'))
#db = db_url.connect(os.environ.get('DATABASE_URL', 'postgresql://localhost:5432/stocker'))


class BaseModel(Model):
    class Meta:
        database = db
        only_save_dirty = True


class Company(BaseModel):
    symbol = CharField(unique=True)
    name = CharField(null=True)
    sector = CharField(null=True)
    industry = CharField(null=True)


class FinancialData(BaseModel):
    company = ForeignKeyField(Company)
    date = DateTimeField(null=True)
    ask = DoubleField(null=True)
    book_value = DoubleField(null=True)
    market_cap = DoubleField(null=True)
    ebitda = DoubleField(null=True)
    pe_ratio_ttm = DoubleField(null=True)
    eps_estimate_qtr = DoubleField(null=True)
    peg_ratio = DoubleField(null=True)
    one_yr_target_price = DoubleField(null=True)
    dividend_yield = DoubleField(null=True)
    return_on_assets = DoubleField(null=True)
    return_on_equity = DoubleField(null=True)
    change_year_low_per = DoubleField(null=True)
    change_year_high_per = DoubleField(null=True)
    one_yr_target_price = DoubleField(null=True)
    dividend_yeild = DoubleField(null=True)
    net_income = DoubleField(null=True)
    total_assets = DoubleField(null=True)
    OneyrTargetPrice = DoubleField(null=True)
    EPSEstimateCurrentYear = DoubleField(null=True)
    EPSEstimateNextYear = DoubleField(null=True)
    EPSEstimateNextQuarter = DoubleField(null=True)

    class Meta:
        indexes = (
            (('company', 'date'), True),
        )


def main():
    tables = [
        Company,
        FinancialData,
    ]
    db.create_tables(tables)


if __name__ == '__main__':
    main()
