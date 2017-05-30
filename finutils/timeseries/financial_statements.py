import arrow
from collections import namedtuple
import funcy
import json
import pandas as pd
import urllib2


BASE_YAHOO_URL = (
    'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules={module}'
)
ALLOWED_STATEMENT_TYPES = {'income_statement', 'cash_flow', 'balance_sheet'}

StatementConfig = namedtuple('statement', ('name', 'module', 'submodule'))

INCOME_STATEMENT_CONFIG = StatementConfig(name='income_statement',
                                          module='incomeStatementHistory',
                                          submodule='incomeStatementHistory')

CASH_FLOW_CONFIG = StatementConfig(name='cash_flow',
                                   module='cashflowStatementHistory',
                                   submodule='cashflowStatements')

BALANCE_SHEET_CONFIG = StatementConfig(name='balance_sheet',
                                       module='balanceSheetHistory',
                                       submodule='balanceSheetStatements')


_statement_type_to_config = {
    'income_statement': INCOME_STATEMENT_CONFIG,
    'cash_flow': CASH_FLOW_CONFIG,
    'balance_sheet': BALANCE_SHEET_CONFIG
}


def _compose_url(ticker, module):
    '''format url for scraping the statement'''
    return BASE_YAHOO_URL.format(ticker=ticker, module=module)


def _get_raw_financials(ticker, statement_type, quarterly):
    if statement_type not in ALLOWED_STATEMENT_TYPES:
        raise ValueError('statement_type {} is not supported'.format(statement_type))
    config = _statement_type_to_config[statement_type]
    module = config.module + 'Quarterly' if quarterly else config.module

    # load url
    url = _compose_url(ticker, module)
    url_open = urllib2.urlopen(url)
    json_str = json.load(url_open)

    raw = funcy.get_in(json_str, ['quoteSummary', 'result', 0, module, config.submodule])
    return raw


def _clean_period_dict(period_dict):
    ''''''
    return {k: v['raw'] for k, v in period_dict.items() if v and isinstance(v, dict)}


def get_financial_statement(ticker, statement_type, quarterly):
    ''''''
    raw_data = _get_raw_financials(ticker, statement_type, quarterly)
    clean_data = map(_clean_period_dict, raw_data)
    df = pd.DataFrame(clean_data)
    df['endDate'] = pd.to_datetime([arrow.get(date).date() for _, date in df.endDate.iteritems()])
    return df.set_index('endDate').transpose()
