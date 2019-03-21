#!/bin/bash

#app_dir='/Users/cfischer/Code/stocker'
app_dir='/srv/stocker'
log_file='/tmp/stocker.log'


cd $app_dir

source venv/bin/activate

python import_financials.py yahoo_finance >> $log_file 2>&1

python import_financials.py yahoo_roa >> $log_file 2>&1

python import_financials.py quandl >> $log_file 2>&1

python calc_financials.py >> $log_file 2>&1


