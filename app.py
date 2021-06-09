from flask import Flask, render_template, request
from patterns import patterns
import yfinance as yf
import os
import csv
import pandas as pd
import talib
app = Flask(__name__)


@app.route("/")
def index():
    pattern = request.args.get('pattern', None)
    stocks = {}
    with open('datasets/companies.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        datafiles = os.listdir('datasets/daily')
        for dataset in datafiles:
            df = pd.read_csv('datasets/daily/{}'.format(dataset))
            patternfunction = getattr(talib, pattern)

            symbol = dataset.split('.')[0]
            try:
                result = patternfunction(
                    df['Open'], df['High'], df['Low'], df['Close'])
                last = result.tail(1).values[0]

                if last > 0:
                    stocks[symbol][pattern] = 'bullish'

                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except:
                pass

        print(datafiles)

    return render_template('index.html', patterns=patterns, stocks=stocks, current_pattern=pattern)


@ app.route('/snapshot')
def snapshot():

    with open('datasets/companies.csv') as f:

        symbols = f.read().splitlines()
        for company in symbols:
            symbol = company.split(',')[0]
            print(symbol)
            data = yf.download(symbol, start="2020-01-01", end="2020-08-01")
            data.to_csv('datasets/daily/{}.csv'.format(symbol))
    return {
        'code': 'success'
    }
