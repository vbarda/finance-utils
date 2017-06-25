import datetime
import pandas as pd
import numpy as np
import unittest

from finutils.utils import column_renamer, lower_func, space_replace_func, get_last_business_day
from finutils.timeseries.quotes import _get_quote_series, get_close


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


class TestQuotes(unittest.TestCase):

    def test__get_quote_series(self):
        ts = _get_quote_series('AAPL', 'Close', '2000-01-01', None)
        max_bdate = get_last_business_day()
        # check dates
        self.assertEqual(ts.index.min(), pd.to_datetime('2001-07-30'))  # min date in Google Finance
        self.assertEqual(ts.index.max(), max_bdate)
        # check columns
        self.assertEqual(ts.columns, 'AAPL')

    def test_close(self):
        aapl = get_close('AAPL')
        self.assertEqual(aapl.columns, 'AAPL')
        self.assertIsInstance(aapl, pd.DataFrame)
        # test multiple tickers
        ts_df = get_close(['AAPL', 'MSFT'])
        self.assertListEqual(ts_df.columns.tolist(), ['AAPL', 'MSFT'])
        self.assertIsInstance(ts_df, pd.DataFrame)
