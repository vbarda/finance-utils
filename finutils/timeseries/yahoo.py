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

def get_yahoo_data(symbol, start_date=None, end_date=None):
    '''Use DataReader functionality to get the timeseries df for a given ticker
    Args:
        symbol: (str) ticker for which to get data
        start_date: (date/str) start date. Defaults to 01/01/2000
        end_date: (date/str) end date. Defaults to today
    '''
    if start_date is None:
        start_date = '2000-01-01'
    if end_date is None:
        end_date = pd.to_datetime(pd.datetime.today(), format='%Y-%m-%d')
    return DataReader(symbol, data_source='yahoo', start=start_date, end=end_date)


def _get_series_from_yahoo(symbol, column, **kwargs):
    '''Wrapper around get_yahoo_data to extract single timeseries
    Args:
        symbol: (str) ticker for which to get yahoo series
        column: (str) series to pick from yahoo output
    '''
    return get_yahoo_data(symbol, **kwargs)[column].to_frame(symbol)


def _get_close(symbol, adjusted=True, **kwargs):
    '''Wrapper around _get_series_from_yahoo to extract close price series
    Args:
        symbol: (str) ticker for which to get close price
        adjusted: (bool) whether to get adj close or close price. Default True
        **kwargs: passed to _get_series_from_yahoo
    '''
    column = 'Adj Close' if adjusted else 'Close'
    return _get_series_from_yahoo(symbol, column=column, **kwargs)


def _get_volume(symbol, **kwargs):
    '''Wrapper around _get_series_from_yahoo to extract volume series
    Args:
        symbol: (str) ticker for which to get volumes
        **kwargs: passed to _get_series_from_yahoo
    '''
    return _get_series_from_yahoo(symbol, column='Volume', **kwargs)


def _get_multiple_timeseries(symbols, ts_getter=_get_close):
    '''Use multiprocessing to get series for multiple symbols'''
    if not hasattr(symbols, '__iter__'):
        symbols = [symbols]
    p = Pool(POOL_CPUS)
    px_dfs = p.map(ts_getter, symbols)
    return pd.concat(px_dfs, axis=1)


def get_close(symbols, adjusted=True, **kwargs):
    '''Creates a combined close prices df for an iterable of tickers
    Args:
        symbols: (str/iterable) of tickers to get the price for
        adjusted: (bool) whether to get adj close or close price. Default True
        **kwargs: passed to get_metrics
    '''
    getter = partial(_get_close, adjusted=adjusted, **kwargs)
    return _get_multiple_timeseries(symbols, getter)


def get_volume(symbols, **kwargs):
    '''Creates a combined volume df for an iterable of tickers
    Args:
        symbols: (str/iterable) of tickers to get the price for
        **kwargs: passed to get_metrics
    '''
    getter = partial(_get_volume, **kwargs)
    return _get_multiple_timeseries(symbols, getter)
