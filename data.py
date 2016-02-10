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

def get_companies():
    return d.Company.select().where(
        ~(d.Company.symbol ** '%^%' | d.Company.symbol ** '%.%'
        | d.Company.symbol ** 'WYY')
    )

def get_tech_companies():
    return d.Company.select().where(
        ~(d.Company.symbol ** '%^%' | d.Company.symbol ** '%.%'
        | d.Company.symbol ** 'WYY')
        & (d.Company.sector == 'Technology')
    )

def set_rank(data):
    rank_pe_ttm = sorted(data, key=operator.itemgetter(2))
    rank_pe_ftm = sorted(data, key=operator.itemgetter(3))
    rank_pe_roa = sorted(data, key=operator.itemgetter(4))
