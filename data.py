import database as d


def save_model(model, kwargs):
    for key, value in kwargs.items():
        setattr(model, key, value)

    model.save()

    return model


def set_company(symbol, **kwargs):
    model, _ = d.Company.get_or_create(symbol=symbol, **kwargs)
    return save_model(model, kwargs)


def set_financial_data(company, symbol, date, **kwargs):
    model, _ = d.FinancialData.create_or_get(company=company, symbol=symbol, date=date, **kwargs)
    return save_model(model, kwargs)


def get_financial_data():
    return d.FinancialData.select()


def get_companies():
    return d.Company.select().where(
        ~(d.Company.symbol ** '%^%' | d.Company.symbol ** '%.%' |
            d.Company.symbol ** 'WYY')
    )


def get_tech_companies():
    return d.Company.select().where(
        ~(d.Company.symbol ** '%^%' | d.Company.symbol ** '%.%' |
            d.Company.symbol ** 'WYY') & (d.Company.sector == 'Technology')
    )


def set_rank(symbol, date, field, rank):
    kwargs = {field: rank}
    model, _ = d.FinancialData.create_or_get(symbol=symbol, date=date, **kwargs)
    return save_model(model, kwargs)


def get_magic_formula_trailing():
    return d.Company.raw(
        '''SELECT company.id, company.symbol,
        financialdata.magic_formula_trailing AS score,
        financialdata.rank_magic_formula_trailing AS rank
        FROM company
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE rank > 0
        ORDER BY rank ASC'''
        )


def get_magic_formula_future():
    return d.Company.raw(
        '''SELECT company.id, company.symbol,
        financialdata.magic_formula_future AS score,
        financialdata.rank_magic_formula_future AS rank
        FROM company
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE rank > 0
        ORDER BY rank ASC'''
        )


def get_ranks(strategy):

    strat = "financialdata." + strategy
    rank = "financialdata.rank_" + strategy
    return d.Company.raw(
        '''SELECT company.id, company.symbol, company.name,
        %s AS score, %s AS rank
        FROM company
        INNER JOIN financialdata on company.id = financialdata.company_id
        WHERE rank > 0
        ORDER BY rank ASC''' % (strat, rank)
        )
