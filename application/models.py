from index import db, bcrypt


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.active = True
        self.password = User.hashed_password(password)

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None


class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer(), primary_key=True)
    symbol = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255))
    sector = db.Column(db.String(255))
    industry = db.Column(db.String(255))
    ask = db.Column(db.Numeric(10,2))
    book_value = db.Column(db.Numeric(10,2))
    market_cap = db.Column(db.Numeric(10,2))
    ebitda = db.Column(db.Numeric(10,2))
    pe_ratio_ttm = db.Column(db.Numeric(10,2))
    pe_ratio_ftm = db.Column(db.Numeric(10,2))
    eps_estimate_qtr = db.Column(db.Numeric(10,2))
    peg_ratio = db.Column(db.Numeric(10,2))
    garp_ratio = db.Column(db.Numeric(10,2))
    return_on_assets = db.Column(db.Numeric(10,2))
    return_on_equity = db.Column(db.Numeric(10,2))
    change_year_low_per = db.Column(db.Numeric(10,2))
    change_year_high_per = db.Column(db.Numeric(10,2))
    net_income = db.Column(db.Numeric(10,2))
    total_assets = db.Column(db.Numeric(10,2))
    shares_outstanding = db.Column(db.Numeric(10,2))
    OneyrTargetPrice = db.Column(db.Numeric(10,2))
    DividendYield = db.Column(db.Numeric(10,2))
    EPSEstimateCurrentYear = db.Column(db.Numeric(10,2))
    EPSEstimateNextYear = db.Column(db.Numeric(10,2))
    EPSEstimateNextQuarter = db.Column(db.Numeric(10,2))
    magic_formula_trailing = db.Column(db.Numeric(10,2))
    magic_formula_future = db.Column(db.Numeric(10,2))


    def __init__(self, symbol):
        self.symbol = symbol


'''class Stockinfo(db.Model):
    __tablename__ = 'stockinfo'
    id = db.Column(db.Integer(), primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.Column(db.String(255), unique=True)
    symbol = db.Column(db.String(255), unique=True)
    date = db.Column(db.Numeric(10,2))
    rank_ask = db.Column(db.Numeric(10,2))
    rank_book_value = db.Column(db.Numeric(10,2))
    rank_market_cap = db.Column(db.Numeric(10,2))
    rank_ebitda = db.Column(db.Numeric(10,2))
    rank_pe_ratio_ttm = db.Column(db.Numeric(10,2))
    rank_pe_ratio_ftm = db.Column(db.Numeric(10,2))
    rank_eps_estimate_qtr = db.Column(db.Numeric(10,2))
    rank_peg_ratio = db.Column(db.Numeric(10,2))
    rank_garp_ratio = db.Column(db.Numeric(10,2))
    rank_return_on_assets = db.Column(db.Numeric(10,2))
    rank_return_on_equity = db.Column(db.Numeric(10,2))
    rank_change_year_low_per = db.Column(db.Numeric(10,2))
    rank_change_year_high_per = db.Column(db.Numeric(10,2))
    rank_net_income = db.Column(db.Numeric(10,2))
    rank_total_assets = db.Column(db.Numeric(10,2))
    rank_OneyrTargetPrice = db.Column(db.Numeric(10,2))
    rank_DividendYield = db.Column(db.Numeric(10,2))
    rank_EPSEstimateCurrentYear = db.Column(db.Numeric(10,2))
    rank_EPSEstimateNextYear = db.Column(db.Numeric(10,2))
    rank_EPSEstimateNextQuarter = db.Column(db.Numeric(10,2))
    rank_magic_formula_trailing = db.Column(db.Numeric(10,2))
    rank_magic_formula_future = db.Column(db.Numeric(10,2))


    def __init__(self, email, password):
        self.email = email
        self.active = True
        self.password = User.hashed_password(password)

    @staticmethod
    def hashed_password(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None
'''
