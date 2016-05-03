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
