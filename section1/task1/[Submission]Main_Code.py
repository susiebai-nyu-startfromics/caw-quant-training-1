# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.tz import tzutc

# %% [markdown]
# #### required output columns info: <br>
# close float64 <br>
# high float64 <br>
# low float64 <br>
# open float64 <br>
# volume float64 <br>
# baseVolume float64 <br>
# datetime object <br>
# dtype: object

# %%
def histohour_main(fsym='BTC', tsym='USDT', start_time='2017-04-01', end_time='2020-04-01', e='binance'):
    #create UTC Unix timestamps from start & end date strings passed in
    req_start_epoch = int(datetime.strptime(start_time, '%Y-%m-%d').replace(tzinfo=tzutc()).timestamp())
    req_end_epoch = int(datetime.strptime(end_time, '%Y-%m-%d').replace(tzinfo=tzutc()).timestamp())

    result_df = pd.DataFrame()
    next_endtime = req_end_epoch     #initialize "end time"
    while True:
        r = requests.get("https://min-api.cryptocompare.com/data/v2/histohour?", params={'fsym':fsym, 'tsym': tsym, 'limit': 2000, 'toTs': str(next_endtime), 'e': e})
        response = r.json()         #the API query response actually can be decoded as a JSON (list of dicts) object!
        current_df = pd.DataFrame(response['Data']['Data']).drop(['conversionType', 'conversionSymbol'], axis=1)
        result_df = pd.concat([current_df, result_df], axis=0, ignore_index=True)   #stack/add the current df to result df along the y-axis
        current_starttime = result_df.time.min()   #check the smallest value in the 'time' column of df as the start time of the current iteration
        next_endtime = current_starttime - 3600    #the end time for the next round is 'one hour'(3600 Unix timestamp units) before the start time of the current iteration
        if current_starttime <= req_start_epoch:
            break

    #result df Data Cleaning
    result_df.sort_values(by="time", inplace=True)     #(just in case)
    result_df = result_df[result_df['time'] >= req_start_epoch]      #delete superfluous data earlier than the required start datetime
    result_df = result_df.rename(columns={'time':'datetime', 'volumefrom':'volume', 'volumeto':'baseVolume'})
    result_df.datetime = result_df.datetime.apply(lambda d: datetime.utcfromtimestamp(d).strftime("%Y/%m/%d %H:%M"))         #(*)change the UTC Unix timestamps display format to be string
    result_df = result_df[["close", "high", "low", "open", "volume", "baseVolume", "datetime"]]
    
    #write the final result dataframe to csv file
    result_df.to_csv("/Users/baixiao/Desktop/S1T1_output.csv", index=False)


# %%
histohour_main()


# %%



