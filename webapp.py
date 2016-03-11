from flask import Flask, render_template, flash                                 
from flask_bootstrap import Bootstrap                                           
from flask_appconfig import AppConfig                                           
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator

from flask_wtf import Form, RecaptchaField                                      
from flask_wtf.file import FileField                                            
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators              
from wtforms.validators import Required

import data

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

    # Install our Bootstrap extension
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
    	score = rank.score
    	) for rank in rankings]
        
        return render_template('results.html', Entries=entries)
    
    
    ## Shows a long signup form, demonstrating form rendering.
    #@frontend.route('/example-form/', methods=('GET', 'POST'))
    #def example_form():
    #    form = SignupForm()
    #
    #    if form.validate_on_submit():
    #        # We don't have anything fancy in our application, so we are just
    #        # flashing a message when a user completes the form successfully.
    #        #
    #        # Note that the default flashed messages rendering allows HTML, so
    #        # we need to escape things if we input user values:
    #        flash('Hello, {}. You have successfully signed up'
    #              .format(escape(form.name.data)))
    #
    #        # In a real application, you may wish to avoid this tedious redirect.
    #        return redirect(url_for('.index'))
    #
    #    return render_template('signup.html', form=form)
    
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=4444, debug=True) 
