'''
    Filename: cv.py
    Author: Vadym Barda <vadim.barda@gmail.com>
    Maintainer: Vadym Barda <vadim.barda@gmail.com>
    URL: https://github.com/vbarda/finance-utils/
'''

import numpy as np
from sklearn.cross_validation import train_test_split

DEFAULT_TRAIN = .7


class CV(object):
    def __init__(self, df, X_cols, y_col, train_size=DEFAULT_TRAIN):
        '''Split the dataframe with features (X_cols) and target (y_col) into
        train and test samples
        Args:
            df: (pd.DataFrame) with features and target
            X_cols: (iterable) of feature columns names
            y_col: (str) target column name
            train_size: (float) the size of the train sample.
                passed to sklearn.cross_validation.train_test_split
        '''
        self.df = df
        self.X_cols = X_cols
        self.X = np.array(df[X_cols])
        self.y = np.array(df[y_col])
        (self.X_tr,
         self.X_te,
         self.y_tr,
         self.y_te) = train_test_split(self.X, self.y, train_size=train_size)
