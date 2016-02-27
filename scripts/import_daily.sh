#!/bin/bash

app_dir='/Users/cfischer/Code/stocker'
log_file='/tmp/stocker.log'


cd $app_dir

source venv/bin/activate

python import_financials.py yahoo_finance >> $log_file

python import_financials.py yahoo_roa >> $log_file

python import_financials.py quandl >> $log_file

python calc_financials.py >> $log_file


