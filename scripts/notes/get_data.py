#!/usr/bin/env python

import json
import urllib2

# get list of tickers from tickers.txt file
def getTickerList():
    with open("tickers.txt") as ftickers:
        ticker_lines = ftickers.readlines()
    ticker_list = []   
    for x in ticker_lines:
        y = x.split(":")
        z = y[0].rstrip()
        ticker_list.append(z)
    return ticker_list

# accept an array of tickers, build a url and query yahoo
def getTickerData(tlist):
    query = ""
    #Don't build a url with more than 100 tickers
    for ticker in tlist[:1000]:
        query = query + "%22" + ticker + "%22,"
    query = query[:-1]
    url = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20IN%20(" + query + ")&format=json&env=http://datatables.org/alltables.env"
    response = urllib2.urlopen(url)
    data = response.read()
    values = json.loads(data)
    return values
   
tickers = getTickerList()

print getTickerData(tickers)
