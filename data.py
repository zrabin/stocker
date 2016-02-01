import database as d 


def save_model(model, kwargs):
    for key, value in kwargs.items():
        setattr(model, key, value)

    model.save()

    return model

def set_company(symbol, **kwargs):
    model, _ = d.Company.get_or_create(symbol=symbol, **kwargs)
    return save_model(model, kwargs)

#def set_financial_data(company, date, **kwargs):
def set_financial_data(company, **kwargs):
#    model, _ = d.FinancialData.create_or_get(company=company, date=date, **kwargs)
    model, _ = d.FinancialData.create_or_get(company=company, **kwargs)
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

