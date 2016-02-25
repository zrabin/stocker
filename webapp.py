#!/usr/bin/env python

import os
import sys
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable

## create our little application :)
#
app.config.update(dict(
    DATABASE = 'stocker.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='user',
    PASSWORD='pass'
))

app.config.from_envvar('STOCKER', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/magic_formula')
def magic_formula():
    db = connect_db()
    cur = db.execute('select company_id, symbol, magic_formula_trailing from financialdata where magic_formula_trailing > 0 order by magic_formula_trailing')

    entries = [dict(ID=row[0], symbol=row[1], magic_formula_trailing=row[2]) for row in cur.fetchall()]
    db.close()
    return render_template('magic_formula.html', Entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('magic_formula'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4444)
