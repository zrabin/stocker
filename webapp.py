import string
import data

from flask import Flask, render_template, flash                                 
from flask_bootstrap import Bootstrap                                           
from flask_appconfig import AppConfig                                           
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator

from flask_wtf import Form, RecaptchaField                                      
from wtforms import TextField, ValidationError, SubmitField, Form, validators              
from wtforms.validators import Required, Email


#form class setup
class SignupForm(Form):
    name = TextField(u'Your name', [validators.required()])
    password = TextField(u'Your favorite password', [validators.required()])
    email = TextField(u'Your email address', [validators.required()])
    submit = SubmitField(u'Signup')


#setup navigation
nav = Nav()
nav.register_element('frontend_top', Navbar(
    View('Stocker', '.index'),
    Subgroup(
        'Rankings',
        View('Magic Formula Trailing', 'rank', strategy = 'magic_formula_trailing'),
        View('Magic Formula Future', 'rank', strategy = 'magic_formula_future'),
        View('Market Cap', 'rank', strategy = 'market_cap'),
        View('EBITDA', 'rank', strategy = 'ebitda'),
        View('PE ratio trailing', 'rank', strategy = 'pe_ratio_ttm'),
        View('PE ratio future', 'rank', strategy = 'pe_ratio_ftm'),
        View('GARP ratio', 'rank', strategy = 'garp_ratio'),
        View('Return on Assets', 'rank', strategy = 'return_on_assets'),
        View('Return on Equity', 'rank', strategy = 'return_on_equity'),
        View('Dividend Yield', 'rank', strategy = 'DividendYield'),
        View('EPS estimate year', 'rank', strategy = 'EPSEstimateCurrentYear'),
        View('EPS estimate next year', 'rank', strategy = 'EPSEstimateNextYear'),
        View('EPS estimate next quarter', 'rank', strategy = 'EPSEStimateNextQuarter'),
        ),
    Subgroup(
        'Development',
        Link('Flask-Bootstrap', 'http://pythonhosted.org/Flask-Bootstrap'),
        Link('Flask-AppConfig', 'https://github.com/mbr/flask-appconfig'),
        Link('Flask-Debug', 'https://github.com/mbr/flask-debug'),
        Separator(),
        Text('Bootstrap'),
        Link('Getting started', 'http://getbootstrap.com/getting-started/'),
        Link('CSS', 'http://getbootstrap.com/css/'),
        Link('Components', 'http://getbootstrap.com/components/'),
        Link('Javascript', 'http://getbootstrap.com/javascript/'),
        Link('Customize', 'http://getbootstrap.com/customize/'),
    ),
))


def create_app(configfile=None):

    app = Flask(__name__)
    Bootstrap(app)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    nav.init_app(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    
    @app.route('/ranks/<strategy>')
    def rank(strategy):
        rankings = data.get_ranks(strategy)
    
        entries = [dict(
    	ID = rank.id, 
    	symbol = rank.symbol, 
    	rank = rank.rank,
    	name = rank.name,
    	score = rank.score,
        link = "http://stockcharts.com/freecharts/perf.php?" + rank.symbol + "&n=200&O=011000",
        pe_ttm = rank.pe_ratio_ttm,
        pe_ftm = rank.pe_ratio_ftm,
        garp = rank.garp,
        peg = rank.peg,
        roa = rank.roa
        #link = "https://www.google.com/finance?q=" + rank.symbol
    	) for rank in rankings]

        strategy = strategy.replace('_', ' ').title()
        
        return render_template('results.html', Entries=entries, Strategy=strategy)
    
    
    ## Shows a long signup form, demonstrating form rendering.
    @app.route('/signup/', methods=('GET', 'POST'))
    def example_form():
        form = SignupForm()
    
    
        return render_template('signup.html', form=form)
    
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=4444, debug=True) 
