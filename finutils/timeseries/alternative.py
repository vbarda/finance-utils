import json
import pandas as pd
import urllib2


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
