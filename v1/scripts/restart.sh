#!/bin/bash

#app_dir='/Users/cfischer/Code/stocker'
app_dir='/srv/stocker'
log_file='/tmp/stocker.log'


cd $app_dir

source venv/bin/activate

ps aux | grep webapp.py | awk {'print $2'} | xargs kill -9

sleep 5 

bash run webapp.py


