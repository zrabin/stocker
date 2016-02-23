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
    symbol = CharField(unique=True)
    date = DateTimeField(null=True)
    ask = DoubleField(null=True)
    book_value = DoubleField(null=True)
    market_cap = DoubleField(null=True)
    ebitda = DoubleField(null=True)
    pe_ratio_ttm = DoubleField(null=True)
    pe_ratio_ftm = DoubleField(null=True)
    eps_estimate_qtr = DoubleField(null=True)
    peg_ratio = DoubleField(null=True)
    garp_ratio = DoubleField(null=True)
    return_on_assets = DoubleField(null=True)
    return_on_equity = DoubleField(null=True)
    change_year_low_per = DoubleField(null=True)
    change_year_high_per = DoubleField(null=True)
    net_income = DoubleField(null=True)
    total_assets = DoubleField(null=True)
    shares_outstanding = DoubleField(null=True)
    OneyrTargetPrice = DoubleField(null=True)
    DividendYield = DoubleField(null=True)
    EPSEstimateCurrentYear = DoubleField(null=True)
    EPSEstimateNextYear = DoubleField(null=True)
    EPSEstimateNextQuarter = DoubleField(null=True)
    magic_formula_trailing = DoubleField(null=True)
    magic_formula_future = DoubleField(null=True)
    
    rank_ask = DecimalField(null=True)
    rank_book_value = DecimalField(null=True)
    rank_market_cap = DecimalField(null=True)
    rank_ebitda = DecimalField(null=True)
    rank_pe_ratio_ttm = DecimalField(null=True)
    rank_pe_ratio_ftm = DecimalField(null=True)
    rank_eps_estimate_qtr = DecimalField(null=True)
    rank_peg_ratio = DecimalField(null=True)
    rank_garp_ratio = DecimalField(null=True)
    rank_return_on_assets = DecimalField(null=True)
    rank_return_on_equity = DecimalField(null=True)
    rank_change_year_low_per = DecimalField(null=True)
    rank_change_year_high_per = DecimalField(null=True)
    rank_net_income = DecimalField(null=True)
    rank_total_assets = DecimalField(null=True)
    rank_OneyrTargetPrice = DecimalField(null=True)
    rank_DividendYield = DecimalField(null=True)
    rank_EPSEstimateCurrentYear = DecimalField(null=True)
    rank_EPSEstimateNextYear = DecimalField(null=True)
    rank_EPSEstimateNextQuarter = DecimalField(null=True)
    rank_magic_formula_trailing = DecimalField(null=True)
    rank_magic_formula_future = DecimalField(null=True)

    class Meta:
        indexes = (
            (('company', 'symbol'), True),
        )


def main():
    tables = [
        Company,
        FinancialData,
    ]
    db.create_tables(tables)


if __name__ == '__main__':
    main()
