import datetime
import pandas as pd
import numpy as np
import unittest

from finutils.utils import column_renamer, lower_func, space_replace_func, get_last_business_day
from finutils.timeseries.yahoo import _get_series_from_yahoo, _get_close, get_close


class TestUtils(unittest.TestCase):

    def test_column_renamer(self):
        df = pd.DataFrame({'Adjusted Close': 2, 'Close': 1}, index=[0, 1])

        renamed_df = column_renamer(df)
        lower_df = column_renamer(df, renamer_func=lower_func)
        space_replace_df = column_renamer(df, renamer_func=space_replace_func)

        self.assertListEqual(['adjusted_close', 'close'],
                              list(renamed_df.columns))
        self.assertListEqual(['adjusted close', 'close'],
                              list(lower_df.columns))
        self.assertListEqual(['Adjusted_Close', 'Close'],
                              list(space_replace_df.columns))


class TestMetrics(unittest.TestCase):

    def test_yahoo_series(self):
        ts = _get_series_from_yahoo('AAPL', 'Close')
        today = pd.to_datetime(datetime.datetime.today()).normalize()
        max_bdate = get_last_business_day(today)
        self.assertEqual(ts.index.min(), pd.to_datetime('2000-01-03'))
        self.assertEqual(ts.index.max(), max_bdate)
        desired_columns = ['Volume', 'Adj Close', 'High', 'Low', 'Close', 'Open']
        self.assertListEqual(sorted(desired_columns), sorted(ts.columns))

class TestPrices(unittest.TestCase):

    def test_close(self):
        aapl = _get_close('AAPL')
        self.assertEqual(aapl.columns, 'AAPL')
        self.assertIsInstance(aapl, pd.DataFrame)
        # test adjusted
        aapl_unadjusted = _get_close('AAPL', adjusted=False)
        self.assertGreater(aapl_unadjusted.AAPL.loc['2016-06-06'], aapl.AAPL.loc['2016-06-06'])
        # test multiple tickers
        ts_df = get_close(['AAPL', 'MSFT'])
        self.assertListEqual(ts_df.columns.tolist(), ['AAPL', 'MSFT'])
        self.assertIsInstance(ts_df, pd.DataFrame)
