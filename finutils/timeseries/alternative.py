import json
import pandas as pd
import threading
import urllib2
import Queue


COMPANY_INFO_URL = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{}?' \
                   'formatted=true&lang=en-US&region=US&modules=assetProfile'


def get_predictwise(link):
    '''Scrape the data from predictwise.com'''
    url = urllib2.urlopen(link)
    json_str = json.load(url)
    df_list = [pd.DataFrame(x.get('table')).assign(date=x.get('timestamp'))
               for x in json_str['history']]
    df = pd.concat(df_list).set_index('date')
    df.index = pd.to_datetime(df.index)
    df.columns = json_str.get('header')
    return df


def _load_company_info(ticker, queue):
    '''helper to load single company info'''
    url_open = urllib2.urlopen(COMPANY_INFO_URL.format(ticker))
    s = json.load(url_open)
    queue.put(s['quoteSummary']['result'][0]['assetProfile'])


def load_multiple_companies_info(tickers):
    '''multiple web requests with threading'''
    queue = Queue.Queue()
    threads = [threading.Thread(target=_load_company_info, args=(ticker, queue))
               for ticker in tickers]
    result = []

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
        result.append(queue.get_nowait())

    return pd.DataFrame(result)
