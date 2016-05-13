import funcy

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
