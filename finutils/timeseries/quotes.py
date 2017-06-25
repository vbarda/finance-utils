'''
    Filename: timeseries.py
    Author: Vadym Barda <vadim.barda@gmail.com>
    Maintainer: Vadym Barda <vadim.barda@gmail.com>
    URL: https://github.com/vbarda/finance-utils/
'''

from funcy import partial
from multiprocessing import Pool
import pandas as pd
from pandas_datareader.data import DataReader

POOL_CPUS = 4


def _get_quote_series(symbol, column, start_date, end_date):
    '''Wrapper around DataReader to extract single timeseries'''
    quote_df = DataReader(symbol, data_source='google', start=start_date, end=end_date)
    return quote_df[column].to_frame(symbol)


def _get_multiple_timeseries(symbols, ts_getter):
    '''Use multiprocessing to get series for multiple symbols'''
    if not hasattr(symbols, '__iter__'):
        symbols = [symbols]
    p = Pool(POOL_CPUS)
    px_dfs = p.map(ts_getter, symbols)
    return pd.concat(px_dfs, axis=1)


# PUBLIC API


def get_close(symbols, start_date=None, end_date=None):
    '''Creates a combined close prices df for an iterable of tickers
    Args:
        symbols: (str/iterable) of tickers to get the price for
        start_date: (date/str) start date. Defaults to 2010-01-01
        end_date: (date/str) end date. Defaults to today
    '''
    getter = partial(_get_quote_series, column='Close', start_date=start_date, end_date=end_date)
    return _get_multiple_timeseries(symbols, getter)


def get_volume(symbols, start_date=None, end_date=None):
    '''Creates a combined volume df for an iterable of tickers
    Args:
        symbols: (str/iterable) of tickers to get the volume for
        start_date: (date/str) start date. Defaults to 2010-01-01
        end_date: (date/str) end date. Defaults to today
    '''
    getter = partial(_get_quote_series, column='Volume', start_date=start_date, end_date=end_date)
    return _get_multiple_timeseries(symbols, getter)
