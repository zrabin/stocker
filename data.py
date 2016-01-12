import database


def save_model(model, kwargs):
    for key, value in kwargs.items():
        setattr(model, key, value)

    model.save()

    return model


def set_company(symbol, **kwargs):
    model, _ = database.Company.create_or_get(symbol=symbol, **kwargs)
    return save_model(model, kwargs)


def set_financial_data(company, date, **kwargs):
    model, _ = database.FinancialData.create_or_get(company=company, date=date, **kwargs)
    return save_model(model, kwargs)


def get_companies():
    return database.Company.select().where(
        ~(database.Company.symbol ** '%^%' | database.Company.symbol ** '%.%')
    )
