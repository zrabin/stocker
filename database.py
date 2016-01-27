#!/usr/bin/env python

import os

from peewee import *
from playhouse import db_url


db = db_url.connect(os.environ.get('DATABASE_URL', 'sqlite:///stocker.db'))


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
    date = DateField()
    ask = DecimalField(null=True)
    book_value = DecimalField(null=True)
    market_cap = DecimalField(null=True)
    ebitda = DecimalField(null=True)
    pe_ratio_ttm = DecimalField(null=True)
    eps_estimate_qtr = DecimalField(null=True)
    peg_ratio = DecimalField(null=True)
    one_yr_target_price = DecimalField(null=True)
    dividend_yield = DecimalField(null=True)
    return_on_assets = DecimalField(null=True)
    return_on_equity = DecimalField(null=True)
    change_year_low_per = DecimalField(null=True)
    change_year_high_per = DecimalField(null=True)
    one_yr_target_price = DecimalField(null=True)
    dividend_yeild = DecimalField(null=True)
    net_income = DecimalField(null=True)
    total_assets = DecimalField(null=True)
    OneyrTargetPrice = DecimalField(null=True)
    EPSEstimateCurrentYear = DecimalField(null=True)
    EPSEstimateNextYear = DecimalField(null=True)
    EPSEstimateNextQuarter = DecimalField(null=True)

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
