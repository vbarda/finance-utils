import pandas as pd

DEFAULT_CREDIT_RATING_URL = 'http://www.tradingeconomics.com/{country}/rating'
DEFAULT_RATING_TABLE_IDX = 0
AGENCIES_OF_INTEREST = ['Fitch', 'S&P', 'Moody\'s']

def _country_to_url(country_str):
    '''preprocess country name for plugging into URL'''
    country_name_substr = map(lambda s: s.lower(), country_str.split(' '))
    return '-'.join(country_name_substr)


def _load_ratings(country_str):
    '''load ratings for country'''
    country_url_str = _country_to_url(country_str)
    url = DEFAULT_CREDIT_RATING_URL.format(country=country_url_str)
    tabs = pd.read_html(url, header=0)
    return tabs[DEFAULT_RATING_TABLE_IDX]


def _post_process_ratings(ratings_df):
    '''cleanup ratings dataframe'''
    return (ratings_df
            .rename(columns=lambda s: s.lower())
            .assign(date=lambda _df: pd.to_datetime(_df.date))
            .loc[lambda _df: _df.agency.isin(AGENCIES_OF_INTEREST)])


def get_ratings_df(country_str):
    '''load and post process ratings data for a specific country'''
    return _load_ratings(country_str).pipe(_post_process_ratings)
