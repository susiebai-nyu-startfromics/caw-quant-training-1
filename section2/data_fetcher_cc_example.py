import os
import datetime
import time
import re

import pandas as pd
import numpy as np
import requests


class CryptoCompareAPI():

    def __init__(self):
        self.url = 'https://min-api.cryptocompare.com/data'

    def _safeRequest(self, url):
        while True:
            try:
                response = requests.get(url)
            except Exception as e:
                print(f'Connection Failed: {e}. Reconnecting...')
                time.sleep(1)
            else:
                break
        resp = response.json()
        if response.status_code != 200:
            raise Exception(resp)
        data = resp['Data']
        return data

    def getCandle(self, fsym, tsym, freq, start_time=None, end_time=None, limit=None, e='CCCAGG'):
        """
            fsym: ticker
            tsym: base
            freq: '1m', '2h', '3d'
            start_time: string datetime format
            end_time: string datetime format
            limit: number of candles
            e: exchange (default:CCCAGG)
        """
        fsym = fsym.upper()
        tsym = tsym.upper()
        agg = re.findall(r"\d+", freq)[0]
        freq = re.findall(r"[a-z]", freq)[0]
        if freq == 'd':
            base_url = "/histoday?fsym={}&tsym={}".format(fsym, tsym)
        elif freq == 'h':
            base_url = "/histohour?fsym={}&tsym={}".format(fsym, tsym)
        elif freq == 'm':
            base_url = "/histominute?fsym={}&tsym={}".format(fsym, tsym)
        else:
            raise ValueError('frequency', freq, 'not supported')
        base_url += f'&aggregate={agg}'  # aggragate
        base_url += f'&e={e}'  # exchange
        if start_time != None and end_time != None and limit == None:
            start_unix = int(pd.to_datetime(start_time).timestamp())
            end_unix = int(pd.to_datetime(end_time).timestamp())
            base_url += f'&limit={2000}'  # limit
            query_url = base_url + f'&toTs={end_unix}'  # until
            bottom_df = pd.DataFrame(self._safeRequest(self.url + query_url))
            if len(bottom_df) == 0:
                raise Exception(f'No Data Fetched with {self.url + query_url}')
            while True:
                old_unix = bottom_df.iloc[0]['time']
                if old_unix <= start_unix:
                    bottom_df = bottom_df[bottom_df['time'] >= start_unix]
                    break
                else:
                    query_url = base_url + f'&toTs={old_unix}'
                    query_df = pd.DataFrame(
                        self._safeRequest(self.url + query_url))
                    if len(query_df) == 0:
                        request_time = datetime.datetime.utcfromtimestamp(
                            start_unix).strftime('%Y-%m-%d %H:%M:%S')
                        earlies_time = datetime.datetime.utcfromtimestamp(
                            old_unix).strftime('%Y-%m-%d %H:%M:%S')
                        print(
                            f"Request from {request_time}. But Available from {earlies_time}")
                        break
                    else:
                        bottom_df = query_df.append(
                            bottom_df.iloc[1:], ignore_index=True)
            return bottom_df
        elif end_time != None and limit != None and start_time == None:
            end_unix = int(pd.to_datetime(end_time).timestamp())
            base_url += f'&limit={limit}'  # limit
            query_url = base_url + f'&toTs={end_unix}'  # until
            return pd.DataFrame(self._safeRequest(self.url + query_url))
        elif end_time == None and start_time == None and limit != None:
            base_url += f'&limit={limit}'  # limit
            return pd.DataFrame(self._safeRequest(self.url + base_url))
        else:
            raise ValueError(
                f"Can't do start_time={start_time}, end_time={end_time}, limit={limit}")


def unix2date(unix, fmt="%Y-%m-%d %H:%M:%S"):
    """
        Convert unix epoch time 1562554800 to
        datetime with format
    """
    date = datetime.datetime.utcfromtimestamp(unix)
    return date.strftime(fmt)


def date2unxi(date, fmt="%Y-%m-%d %H:%M:%S"):
    """
        Convert datetime with format to 
        unix epoch time 1562554800
    """
    return int(time.mktime(time.strptime(date, fmt)))


def cc2bt(df):
    """Convert CryptoCompare data to Backtrader data
    """
    df['datetime'] = df['time'].apply(unix2date)
    df.drop(columns=['time'], inplace=True)
    df.rename(columns={'volumefrom': 'volume',
                       'volumeto': 'baseVolume'}, inplace=True)
    return df


cc_api = CryptoCompareAPI()
DATA_DIR = './data'

df = cc_api.getCandle('BTC', 'USDT', '1h', start_time="2017-04-01",
                      end_time="2020-08-22", e='binance')
df = cc2bt(df)
df.to_csv(os.path.join(DATA_DIR, "BTC_USDT_1h.csv"), index=False)
