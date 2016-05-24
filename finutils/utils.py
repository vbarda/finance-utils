import funcy
import pandas as pd

lower_func = lambda x: x.lower()
space_replace_func = lambda x: x.replace(' ', '_')
lower_replace_func = funcy.compose(lower_func, space_replace_func)


def column_renamer(df, renamer_func=lower_replace_func):
    '''Rename df columns using the renamer function
    Args:
        df: (pd.DataFrame)
        renamer_func: (function) used for renaming the columns
    '''
    new_columns = map(renamer_func, df.columns)
    return df.rename(columns={k: v for k, v in zip(df.columns,
                                                   new_columns)})


def split_to_numeric(ser, delim=' ', side=0):
    '''Split the series values by delimiter, pick left (0) or right (1) side
    of the split and convert it to numeric
    Args:
        ser: (pd.Series) to split and convert to numeric
        delim: (str) delimiter to split the string on
        side: (int) left (0) or right (1) side of the split
    '''
    return ser.apply(lambda x: pd.to_numeric(x.split(delim)[side]))
