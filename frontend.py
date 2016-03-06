# This contains our frontend; since it is a bit messy to use the @app.route
# decorator style when using application factories, all of our routes are
# inside blueprints. This is the front-facing blueprint.
#
# You can find out more about blueprints at
# http://flask.pocoo.org/docs/blueprints/

import sqlite3

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape

from forms import SignupForm
from nav import nav

frontend = Blueprint('frontend', __name__)

# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
nav.register_element('frontend_top', Navbar(
    View('Stocker', '.index'),
    View('Magic Formula', '.results'),
#    View('Forms Example', '.example_form'),
    Subgroup(
        'Development',
        View('Debug-Info', 'debug.debug_root'),
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

def connect_db():
    return sqlite3.connect('stocker/stocker.db')

# Our index-page just shows a quick explanation. Check out the template
# "templates/index.html" documentation for more details.
@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/results')
def results():
    db = connect_db()
    cur = db.execute(
	'''SELECT company_id, symbol, magic_formula_trailing, rank_magic_formula_trailing 
	FROM financialdata 
	WHERE magic_formula_trailing > 0 
	ORDER BY magic_formula_trailing'''
	)

    entries = [dict(
	ID = row[0], 
	symbol = row[1], 
	strategy = row[2],
	rank = row[3],
	) for row in cur.fetchall()]
    db.close()
    return render_template('results.html', Entries=entries)

# Shows a long signup form, demonstrating form rendering.
@frontend.route('/example-form/', methods=('GET', 'POST'))
def example_form():
    form = SignupForm()

    if form.validate_on_submit():
        # We don't have anything fancy in our application, so we are just
        # flashing a message when a user completes the form successfully.
        #
        # Note that the default flashed messages rendering allows HTML, so
        # we need to escape things if we input user values:
        flash('Hello, {}. You have successfully signed up'
              .format(escape(form.name.data)))

        # In a real application, you may wish to avoid this tedious redirect.
        return redirect(url_for('.index'))

    return render_template('signup.html', form=form)
