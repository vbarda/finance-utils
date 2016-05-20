import datetime
import pandas as pd
import numpy as np
import unittest

from finutils.utils import column_renamer, lower_func, space_replace_func
from finutils.ingest.timeseries import get_metrics
from finutils.sk_utils.cv import CV


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

    def test_metrics(self):
        ts = get_metrics('AAPL')
        today = datetime.datetime.today()
        correct_date = (today + datetime.timedelta(-1) if today.hour < 16
                                                       else today)
        self.assertEqual(ts.index.min(), pd.to_datetime('2000-01-03'))
        self.assertEqual(ts.index.max(),
                         pd.to_datetime(correct_date).normalize())
        desired_columns = ['Volume', 'Adj Close', 'High', 'Low', 'Close', 'Open']
        self.assertListEqual(sorted(desired_columns), sorted(ts.columns))


class TestCV(unittest.TestCase):

    def test_split(self):
        df = get_metrics('AAPL').pipe(column_renamer)
        X_cols = df.columns.drop('close')
        cv = CV(df, X_cols=X_cols, y_col='close', train_size=.8)
        self.assertTupleEqual(df.drop('close', 1).shape, cv.X.shape)
        self.assertTupleEqual(
            np.concatenate([cv.X_tr, cv.X_te]).shape, cv.X.shape
        )
