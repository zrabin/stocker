#!/usr/bin/env python

import os

from peewee import *
from playhouse import db_url


db = db_url.connect(os.environ.get('DATABASE_URL', 'sqlite:///stocker.db'))


class BaseModel(Model):
    class Meta:
        database = db


class Company(BaseModel):
    symbol = CharField(unique=True)
    name = CharField(null=True)
    sector = CharField(null=True)
    industry = CharField(null=True)


class FinancialData(BaseModel):
    company = ForeignKeyField(Company)
    date = DateField()
    book_value = DecimalField(null=True)
    market_cap = DecimalField(null=True)
    ebitda = DecimalField(null=True)
    pe_ratio = DecimalField(null=True)
    peg_ratio = DecimalField(null=True)
    one_yr_target_price = DecimalField(null=True)
    dividend_yield = DecimalField(null=True)

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
