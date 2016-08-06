'''
    Filename: timeseries.py
    Author: Vadym Barda <vadim.barda@gmail.com>
    Maintainer: Vadym Barda <vadim.barda@gmail.com>
    URL: https://github.com/vbarda/finance-utils/
'''

import datetime
import json
import urllib2
import pandas as pd
from ystockquote import get_historical_prices

def get_metrics(symbol, start_date=None, end_date=None, ts_getter=get_historical_prices):
    '''Use ystockquote functionality to get the timeseries df for a given ticker
    Args:
        symbol: ticker for which to get the metric
        start_date: (date/str) start date. Defaults to 01/01/2000
        end_date: (date/str) end date. Defaults to today
        ts_getter: (function) ystockquote function that returns dictionary
    '''
    if start_date is None:
        start_date = '2000-01-01'
    if end_date is None:
        end_date = pd.to_datetime(datetime.datetime.today()).strftime('%Y-%m-%d')
    ts_dict = ts_getter(symbol, start_date, end_date)
    ts_df = pd.DataFrame.from_dict(ts_dict, orient='index').astype(float)
    ts_df.index = pd.to_datetime(ts_df.index)
    return ts_df


def get_close(symbol, adjusted=True, **kwargs):
    '''Get series of close/adjusted close prices from ystockquote
    Args:
        symbol: (str) ticker for which to get close price
        adjusted: (bool) whether to get adj close or close price. Default True
        **kwargs: passed to get_metrics
    '''
    return get_metrics(symbol, **kwargs)['Adj Close' if adjusted else 'Close'].to_frame(symbol)


def get_closes(symbols, adjusted=True, **kwargs):
    '''Creates a combined close prices df for an iterable of tickers
    Args:
        symbols: (str/iterable) of tickers to get the price for
        adjusted: (bool) whether to get adj close or close price. Default True
        **kwargs: passed to get_metrics
    '''
    if not hasattr(symbols, '__iter__'):
        symbols = [symbols]
    return  pd.concat([get_close(symbol, adjusted=adjusted, **kwargs)
                       for symbol in symbols], axis=1)


def get_predictwise(link):
    '''Scrape the data from predictwise.com'''
    url = urllib2.urlopen(link)
    json_str = json.load(url)
    df_list = [pd.DataFrame(x.get('table')).assign(date=x.get('timestamp'))
               for x in json_str['history']]
    df = pd.concat(df_list).set_index('date')
    df.index = pd.to_datetime(df.index)
    df.columns = json_str.get('header')
    return df
