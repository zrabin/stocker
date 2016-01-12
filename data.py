import database


def save_model(model, kwargs):
    for key, value in kwargs.items():
        setattr(model, key, value)

    model.save()


def set_company(symbol, **kwargs):
    model, created = database.Company.create_or_get(symbol=symbol, **kwargs)

    if not created:
        save_model(model, kwargs)

    return model


def set_financial_data(company, date, **kwargs):
    model, created = database.FinancialData.create_or_get(company=company, date=date, **kwargs)

    if not created:
        save_model(model, kwargs)

    return model


def get_companies():
    return database.Company.select().where(
        ~(database.Company.symbol ** '%^%' | database.Company.symbol ** '%.%')
    )
