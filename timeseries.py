import datetime
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
        start_date = pd.to_datetime('2000-01-01').strftime('%Y-%m-%d')
    if end_date is None:
        end_date = pd.to_datetime(datetime.datetime.today()).strftime('%Y-%m-%d')
    ts_dict = ts_getter(symbol, start_date, end_date)
    ts_df = pd.DataFrame.from_dict(ts_dict, orient='index').astype(float)
    ts_df.index = pd.to_datetime(ts_df.index)
    return ts_df


def combine_metrics(symbols, col_name='Adj Close', **kwargs):
    # TODO: add test
    '''Creates a combined df for an iterable of tickers by picking
    specific column from get_metrics output
    Args:
        symbols: (str/iterable) of tickers to get the metric for
        col_name: (str) name of column from the get_metrics output to be used.
            Defaults to 'Adj Close'
        **kwargs: start_date, end_date and ts_getter(ystockquote function) for get_metrics
    '''
    if isinstance(symbols, str) or isinstance(symbols, unicode):
        symbols = [symbols]
    else:
        symbols = list(symbols)
    return pd.DataFrame.from_dict({symbol: get_metrics(symbol, **kwargs)[col_name]
                                   for symbol in symbols})
